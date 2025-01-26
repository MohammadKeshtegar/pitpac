VIDEO_CODEC_GUIDE = """
Codec for videos:
1 - libx264 (H.264): One of the most popular video codecs, widely used for its balance of quality and compression.
2 - libx265 (H.265/HEVC): Successor to H.264, offering better compression and quality at the cost of increased computational power.
3 - libvpx (VP8/VP9): Developed by Google, commonly used for web video (e.g., YouTube).
4 - libaom (AV1): An open and royalty-free codec developed by the Alliance for Open Media, offering even better compression than VP9 and H.265.
5 - mpeg2video (MPEG-2): An older codec still used in DVDs and some broadcast TV.
6 - prores (ProRes): A high-quality codec developed by Apple, often used in professional video editing.
"""

AUDIO_CODEC_GUIDE = """
Codec for audios:
1 - acc AAC (Advanced Audio Codec): Widely used in streaming and storage, known for its high quality and efficiency.
2 - libmp3lame MP3: One of the most popular audio codecs, known for its compatibility and moderate quality.
3 - libopus Opus: An open and versatile codec suitable for both voice and music, known for its low latency.
4 - flac FLAC (Free Lossless Audio Codec): Provides lossless compression, preserving audio quality.
5 - libvorbis Vorbis: An open-source codec, often used in Ogg containers, known for good quality and efficiency.
6 - ac3 AC3 (Dolby Digital): Commonly used in DVDs and Blu-rays, providing surround sound.
"""

VIDEO_BITRATE_GUIDE = """
Bitrate for libx264:
1 - Low Resolution (360p): 500 - 1000 kbps
2 - Standard Definition (480p): 1000 - 2000 kbps
3 - High Definition (720p): 2000 - 4000 kbps
4 - Full HD (1080p): 4000 - 8000 kbps
5 - 4K (2160p): 20000 - 40000 kbps

Bitrate for libx265;
1 - Low Resolution (360p): 250 - 750 kbps
2 - Standard Definition (480p): 500 - 1500 kbps
3 - High Definition (720p): 1500 - 3000 kbps
4 - Full HD (1080p): 3000 - 6000 kbps
5 - 4K (2160p): 10000 - 20000 kbps

Bitrate for VP9 (libvpx-vp9):
1 - Low Resolution (360p): 250 - 750 kbps
2 - Standard Definition (480p): 500 - 1500 kbps
3 - High Definition (720p): 1500 - 3000 kbps
4 - Full HD (1080p): 3000 - 6000 kbps
5 - 4K (2160p): 10000 - 20000 kbps

Bitrate for AV1 (libaom-av1):
1 - Low Resolution (360p): 200 - 600 kbps
2 - Standard Definition (480p): 400 - 1200 kbps
3 - High Definition (720p): 1200 - 2400 kbps
4 - Full HD (1080p): 2400 - 4800 kbps
5 - 4K (2160p): 8000 - 16000 kbps
"""

AUDIO_BITRATE_GUIDE = """
Bitrate for AAC (Advanced Audio Codec):
1 - Low Quality: 64-96 kbps (suitable for voice recordings)
2 - Medium Quality: 128-192 kbps (suitable for general music listening)
3 - High Quality: 256-320 kbps (near CD quality)

Bitrate for MP3 (MPEG Audio Layer III):
1 - Low Quality: 64-96 kbps (suitable for voice recordings)
2 - Medium Quality: 128-192 kbps (suitable for general music listening)
3 - High Quality: 256-320 kbps (near CD quality)

Bitrate for Opus:
1 - Voice: 6-12 kbps (for low bitrate voice)
2 - Low Quality Music: 32-48 kbps
3 - Medium Quality Music: 64-96 kbps
4 - High Quality Music: 128 kbps and above (near CD quality)

Bitrate for Vorbis:
1 - Low Quality: 64-128 kbps
2 - Medium Quality: 128-192 kbps
3 - High Quality: 192-320 kbps

FLAC (Free Lossless Audio Codec):
1 - Lossless Compression: Bitrate varies depending on the source material, but typically ranges from 500 kbps to over 1000 kbps. 
2 - FLAC maintains the original quality and is suitable for high-fidelity audio.
"""

RESOLUTION_GUIDE = """
Standard Definitions (SD)
1 - 240p: 426x240
2 - 360p: 640x360
3 - 480p: 854x480

High Definition (HD)
1 - 720p: 1280x720
2 - 1080p (Full HD): 1920x1080

Ultra High Definition (UHD)
1 - 1440p (2K): 2560x1440
2 - 2160p (4K): 3840x2160
3 - 4320p (8K): 7680x4320

"""

FRAME_RATE_GUIDE = """
Standard Frame Rates
1 - 24 fps: Commonly used for movies and cinematic content. This frame rate gives a film-like quality.
2 - 25 fps: Standard for PAL (Phase Alternating Line) video, which is used in many parts of the world, including Europe and parts of Asia.
3 - 30 fps: Standard for NTSC (National Television System Committee) video, which is used in North America and parts of Asia.
4 - 60 fps: Often used for high-definition video, fast-action scenes, and sports broadcasts. Provides smoother motion.

High Frame Rates (HFR)
1 - 120 fps: Used for slow-motion videos and some high-end video applications. Offers very smooth motion and is useful for action-packed scenes.
2 - 240 fps and above: Used for ultra slow-motion captures, often in sports and scientific applications. These frame rates can capture extremely fast movements and are typically played back at lower frame rates to show the action in slow motion.

Lower Frame Rates
1 - 12-15 fps: Sometimes used for animations or webcam video. Provides a lower-quality motion, but can be sufficient for certain types of content.
2 - 10 fps or less: Used for time-lapse photography and certain types of surveillance footage.
"""