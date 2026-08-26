import os
import time
import base64
from flask import request, jsonify



def validate_face():
    from main import (
        UPLOAD_FOLDER,
        face_validator,
        vggface_shape_classifier
    )
    # THREAD_HOLD is the minimum confidence score required to pass the face validation
    THRESHOLD = 0.4
    """
    Pre-analysis face check using FaceValidator.
    Accepts a multipart image, saves it to a temp file, runs validation,
    then deletes the temp file.
    Returns: {"valid": bool, "message": str, "face_count": int, "error": str|None}
    """
    if 'image' not in request.files or request.files['image'].filename == '':
        return jsonify({'valid': False, 'message': 'No image provided.'}), 400

    file = request.files['image']

    # Save to a temp path so FaceValidator can read it from disk
    timestamp = int(time.time() * 1000)
    tmp_filename = f"_face_check_{timestamp}.jpg"
    tmp_filepath = os.path.join(UPLOAD_FOLDER, tmp_filename)

    try:
        file.save(tmp_filepath)

        if face_validator is None:
            # Validator unavailable — fail open so UX isn't blocked
            return jsonify({'valid': True, 'message': 'Validation skipped (validator unavailable).'})

        result = face_validator.validate(tmp_filepath)

        # Check Face Shape Confidence Threshold
        if result['valid'] and vggface_shape_classifier:
            shape_result = vggface_shape_classifier.classify(tmp_filepath)
            if "error" not in shape_result:
                confidence = shape_result.get("confidence", 0.0)
                if confidence < THRESHOLD:
                    result['valid'] = False
                    result['error'] = "UNCERTAIN FACE TYPE"
                    # Update message so the frontend warning banner shows this specific issue
                    result['message'] = f"Face is unclear (Confidence: {int(confidence * 100)}%). Please look straight into the camera and ensure good lighting."

        return jsonify({
            'valid':      result['valid'],
            'error': result['error'],
            'message':    result['message'],
            'face_count': result.get('face_count', 0),
            'error':      result.get('error')
        })

    except Exception as e:
        print(f"[validate-face] Error: {e}")
        return jsonify({'valid': False, 'message': 'Could not process the image. Please try another photo.'}), 500

    finally:
        # Always clean up the temp file
        if os.path.exists(tmp_filepath):
            try:
                os.remove(tmp_filepath)
            except OSError:
                pass


def analyze():
    from main import (
        UPLOAD_FOLDER,
        vggface_shape_classifier,
        skin_tone_service,
        hairstyle_service
    )
    gender        = request.form.get('gender', 'female')
    analysis_type = request.form.get('analysis_type', 'hairstyle')

    # ── Save uploaded image ─────────────────────────────────────────────────
    timestamp = int(time.time())
    filename  = f"user_photo_{timestamp}.jpg"
    filepath  = os.path.join(UPLOAD_FOLDER, filename)
    saved_url = f"/static/uploads/{filename}"

    existing_image_url = request.form.get('existing_image_url')

    if 'image' in request.files and request.files['image'].filename != '':
        request.files['image'].save(filepath)
    elif 'image_base64' in request.form and request.form['image_base64'].strip():
        base64_data = request.form['image_base64']
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        try:
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(base64_data))
        except Exception as e:
            print("Error decoding base64 image:", e)
            saved_url = ''
    elif existing_image_url:
        import urllib.parse
        parsed = urllib.parse.urlparse(existing_image_url)
        filename_only = os.path.basename(parsed.path)
        filepath = os.path.join(UPLOAD_FOLDER, filename_only)
        if os.path.exists(filepath):
            saved_url = existing_image_url
        else:
            return jsonify({"status": "error", "message": "Image not found."}), 404
    else:
        saved_url = ''

    # ── AI Face Shape Detection ────────────────────────────────────────────
    detected_shape = "oval"   # default fallback
    confidence     = 0.0

    if analysis_type == 'hairstyle':
        from main import face_validator
        if face_validator:
            val_res = face_validator.validate(filepath)
            if not val_res.get('valid'):
                return jsonify({
                    "status": "error", 
                    "message": val_res.get('message', "No face detected. Please retake the photo.")
                }), 400

    if vggface_shape_classifier and os.path.exists(filepath):
        shape_result = vggface_shape_classifier.classify(filepath)
        if "error" in shape_result:
            print(f"[FaceShapeClassifier] {shape_result['error']}")
        else:
            detected_shape = shape_result["face_shape"].lower()
            confidence     = shape_result["confidence"]
            print(f"\n{'='*40}")
            print(f"  Face Shape : {shape_result['face_shape']}")
            print(f"  Confidence : {confidence * 100:.1f}%")
            print(f"{'='*40}\n")
            
            if analysis_type == 'hairstyle' and confidence < 0.4:
                return jsonify({
                    "status": "error", 
                    "message": f"Face shape is unclear (Confidence: {int(confidence * 100)}%). Please retake a clear photo."
                }), 400

    # ── AI Skin Tone Detection (STUB — replace with real model) ────────────
    # TODO: Replace with skin_tone_classifier module.
    # from modules.skin_tone_classifier import SkinToneClassifier
    # undertone = SkinToneClassifier().predict(filepath)
    undertone = "Warm Autumn"
    color_confidence = 0.90  # ← stub
    if skin_tone_service and os.path.exists(filepath):
        analysis_res = skin_tone_service.analyze_image(filepath)
        if analysis_res.get("status") == "success":
            undertone = analysis_res.get("undertone", "warm")
            color_confidence = analysis_res.get("confidence", 0.90)

    # ── Log analysis session ────────────────────────────────────────────────
    hairstyle_service.log_user_analysis(
        user_image_url=saved_url,
        detected_shape=detected_shape,
        gender=gender,
        analysis_type=analysis_type,
        confidence=confidence
    )

    # ── Build redirect URL ──────────────────────────────────────────────────
    if analysis_type == 'hairstyle':
        redirect_url = (
            f"/recommendation?user_img={saved_url}"
            f"&shape={detected_shape}&gender={gender}"
            f"&confidence={confidence}"
            f"&gender={gender}"
        )
    else:
        redirect_url = (
            f"/color-analysis?user_img={saved_url}"
            f"&undertone={undertone}&gender={gender}"
            f"&confidence={color_confidence}"
        )

    # final_confidence = color_confidence if analysis_type == 'color' else confidence

    return jsonify({
        "status":             "success",
        "detected_face_shape": detected_shape,
        "face_shape_title":    detected_shape.capitalize() + " Face",
        "undertone":           undertone,
        "confidence":          confidence,
        "user_image_url":      saved_url,
        "gender":              gender,
        "analysis_type":       analysis_type,
        "redirect_url":        redirect_url
    })
