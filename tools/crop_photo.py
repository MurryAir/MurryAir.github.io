from PIL import Image, ImageOps
import os

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC = os.path.join(ROOT, 'photos', 'Mu Jia.jpg')
BACKUP = os.path.join(ROOT, 'photos', 'Mu Jia.original.jpg')
TARGET_W, TARGET_H = 280, 280


def center_crop_cover(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    # respect EXIF orientation
    img = ImageOps.exif_transpose(img)
    w, h = img.size
    target_ratio = target_w / target_h
    src_ratio = w / h if h else 1.0
    if src_ratio > target_ratio:
        # too wide: crop width
        new_w = int(h * target_ratio)
        left = max((w - new_w) // 2, 0)
        box = (left, 0, left + new_w, h)
    else:
        # too tall: crop height
        new_h = int(w / target_ratio)
        top = max((h - new_h) // 2, 0)
        box = (0, top, w, top + new_h)
    cropped = img.crop(box)
    resized = cropped.resize((target_w, target_h), Image.LANCZOS)
    return resized


def main():
    if not os.path.exists(SRC):
        raise FileNotFoundError(f"Source photo not found: {SRC}")
    # backup original once
    try:
        if not os.path.exists(BACKUP):
            os.replace(SRC, BACKUP)
        else:
            # if backup exists, read from backup to avoid repeated re-cropping
            pass
    except Exception:
        # if replace fails, fall back to copying logic
        if not os.path.exists(BACKUP):
            with open(SRC, 'rb') as r, open(BACKUP, 'wb') as w:
                w.write(r.read())

    src_path = BACKUP if os.path.exists(BACKUP) else SRC
    with Image.open(src_path) as img:
        out = center_crop_cover(img, TARGET_W, TARGET_H)
        # preserve metadata and save at max quality without extra compression
        exif = img.info.get('exif')
        icc = img.info.get('icc_profile')
        out = out.convert('RGB')
        save_kwargs = {}
        if exif:
            save_kwargs['exif'] = exif
        if icc:
            save_kwargs['icc_profile'] = icc
        out.save(
            SRC,
            format='JPEG',
            quality=100,
            subsampling=0,
            optimize=False,
            progressive=False,
            **save_kwargs,
        )
        print(f"Cropped and replaced photo at: {SRC}")


if __name__ == '__main__':
    main()