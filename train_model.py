from src.smart_scheduler_ml import train_model


def main() -> None:
    model = train_model()
    print(
        f"Malli päivitetty onnistuneesti. Opetusnäytteitä käytettiin {model['sample_count']} kappaletta."
    )


if __name__ == "__main__":
    main()
