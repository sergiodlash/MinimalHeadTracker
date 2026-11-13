# Minimal Head Tracker

Quick webcam-based head tracker that streams head rotation (yaw, pitch, roll in degrees) over OSC. Uses the MediaPipe Face Landmarker runs offline on-device.

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

On the cv window use the keys c to recente
**Keys:** `c` = recenter (zero the current pose), `q` = quit

## OSC output

OSC messages to every port in the list `OSC_PORTS` on `OSC_IP`.

| Address | Arguments                         |
|---------|-----------------------------------|
| `/ypr`  | 3 floats: `yaw`, `pitch`, `roll` in degrees |

