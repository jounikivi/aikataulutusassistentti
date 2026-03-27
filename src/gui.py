try:
    from .gui_ai_predict import main
except ImportError:
    from gui_ai_predict import main


if __name__ == "__main__":
    main()
