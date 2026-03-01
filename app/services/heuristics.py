from PIL import Image, ImageFilter
import numpy as np

def _wcag_contrast(fg_rgb, bg_rgb):
    # relative luminance
    def lum(c):
        arr = np.array(c)/255.0
        def srgb_to_lin(x): return x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4
        R,G,B = map(srgb_to_lin, arr)
        return 0.2126*R + 0.7152*G + 0.0722*B
    L1, L2 = lum(fg_rgb), lum(bg_rgb)
    L1, L2 = max(L1, L2), min(L1, L2)
    return (L1 + 0.05) / (L2 + 0.05)

def _detect_low_global_contrast(img):
    # quick global check using RMS contrast proxy
    arr = np.array(img.convert("L"), dtype=np.float32)
    rms = arr.std()  # proxy for contrast
    return rms < 35.0, rms  # threshold tuned empirically

def _detect_edge_overlap_regions(img):
    # Approx: regions with excessive edge density may indicate overlap
    arr = np.array(img.convert("L"))
    edges = Image.fromarray(arr).filter(ImageFilter.FIND_EDGES)
    e = np.array(edges, dtype=np.float32) / 255.0
    # sliding window density
    H, W = e.shape
    win, step, thr = 64, 32, 0.28
    issues = []
    for y in range(0, H-win, step):
        for x in range(0, W-win, step):
            patch = e[y:y+win, x:x+win]
            dens = (patch > 0.3).mean()
            if dens > thr:
                issues.append({
                    "id": f"ovlp:{x}:{y}",
                    "type": "text_overlap",
                    "bbox": [x, y, x+win, y+win],
                    "severity": "medium",
                    "confidence": min(0.95, 0.5 + (dens-thr)),
                    "evidence": f"edge_density={dens:.2f}",
                    "message": "Possible overlapping or cluttered UI region.",
                    "recommendation": "Increase spacing; review z-index/layering."
                })
    return issues

def run_heuristics(img):
    issues = []
    # 1) Global low-contrast screen (useful for dark-on-dark mistakes)
    lowc, rms = _detect_low_global_contrast(img)
    if lowc:
        issues.append({
            "id": "low_contrast:global",
            "type": "low_contrast",
            "bbox": None,
            "severity": "medium",
            "confidence": 0.8,
            "evidence": f"rms={rms:.1f}",
            "message": "Overall low visual contrast detected.",
            "recommendation": "Increase text/background contrast per WCAG AA."
        })

    # 2) Edge-density hotspots → proxy for overlaps / truncation
    issues.extend(_detect_edge_overlap_regions(img))
    return issues