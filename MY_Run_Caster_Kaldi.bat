@echo off
echo Running Kaldi from Dragonfly CLI

set currentpath=%~dp0

TITLE Caster: Status Window
C:\Python38x64\python.exe -m dragonfly load _*.py --engine kaldi --engine-options "model_dir=C:\kaldi_model, audio_self_threaded=False, audio_auto_reconnect=True, vad_padding_start_ms=100, vad_padding_end_ms=200, vad_complex_padding_end_ms=600, invalidate_cache=True, auto_add_to_user_lexicon=True, allow_online_pronunciations=False, lazy_compilation=True, vad_aggressiveness=3, expected_error_rate_threshold=0.1"

pause 1
