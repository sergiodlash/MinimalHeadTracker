# Minimal head tracker

Quick webcam-based head tracker that streams head rotation (yaw, pitch, roll in degrees) over OSC. Uses the MediaPipe Face Landmarker and runs offline on-device.

## Setup

```
conda env create -f environment.yml
```

## Run

```
conda activate headtracker
python tracker.py
```

- On the first run, the face model (`face_landmarker.task`, ~4 MB) is downloaded into the current folder.
- On macOS, you have to grant permission for camera.

**Keys** (in the preview window): `c` = recenter (zero the current pose), `q` = quit

## OSC output

OSC messages to every port in the list `OSC_PORTS` on `OSC_IP`.

| Address | Arguments                         |
|---------|-----------------------------------|
| `/ypr`  | 3 floats: `yaw`, `pitch`, `roll` in degrees |

## Citation

If you use this in your work, please cite it (see `CITATION.cff`, or GitHub's "Cite this repository" button):

```bibtex
@software{delasheras_minimal_head_tracker_2026,
  author = {de las Heras, Sergio},
  title  = {Minimal Head Tracker},
  year   = {2026}
}
```

Head pose estimation is done by [MediaPipe Face Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker) (Apache 2.0).

## License

MIT. See [LICENSE](LICENSE).

