from src.client import chat


CONTEXT: list[dict] = []

while True:
    try:
        user_prompt = input(">> ")
        CONTEXT.append({"role": "user", "content": user_prompt})
        response = chat(CONTEXT, "generous")
        CONTEXT.append({"role": "assistant", "content": response})

        print(response)

    except KeyboardInterrupt:
        print("Exiting..")
        break
