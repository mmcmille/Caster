@echo off
echo Running Kaldi from Dragonfly CLI

set currentpath=%~dp0

TITLE Caster: Status Window
python -m dragonfly load _*.py --engine kaldi --engine-options "model_dir=C:\kaldi_model_daanzu_20211030-smalllm, audio_self_threaded=False, audio_auto_reconnect=True, vad_padding_start_ms=50, vad_padding_end_ms=80, vad_complex_padding_end_ms=200, invalidate_cache=True, auto_add_to_user_lexicon=True, allow_online_pronunciations=False, lazy_compilation=True, vad_aggressiveness=1, expected_error_rate_threshold=0.2"

pause 1
