from openai import OpenAI
import time
from my_keys import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def create_thread():
    try:
        thread = client.beta.threads.create()
        print("Thread ID:", thread)        
        return thread.id
    
    except Exception as e:
        print("Error al crear hilo y mensaje:", e)
        return None

    
def run_prompt(thread_id, prompt_textplain, ASSISTANT_TOKEN): 
    
    try: 
        print("empezando run_prompt")
        client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= prompt_textplain,
        )
        print("Mensaje enviado al hilo.")

        run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=ASSISTANT_TOKEN 
            )
        print("Ejecución creada.")
        while True:
            try:
                keep_retrieving_run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                print("Ejecución recuperada.")
                if keep_retrieving_run.status == 'failed':
                    print("\nLa ejecución ha fallado.")
                    print("Error Message keep_retrieving_run: ", keep_retrieving_run.last_error.message)
                    raise RuntimeError("La ejecución ha fallado.")

                elif keep_retrieving_run.status == "completed":
                    print("\nLa ejecución ha sido completada.")
                    break

                else:
                    time.sleep(3)
                
                print("Ejecución status:", keep_retrieving_run.status)

            except Exception as e:
                print("Error al recuperar la ejecución:", e)
                raise RuntimeError("Error al recuperar la ejecución.")
            


        response_openai = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        if response_openai.data:
            if response_openai.data[0].content:
                content = response_openai.data[0].content
                response = content[0].text.value
                return response
            else:
                print("No hay contenido en el 'response_openai.data' list.")
        else:
            print("No hay contenido en el 'response_openai' list.")

    except Exception as e:
        print("Error en la funcion run_prompt:", e)
        raise RuntimeError("Error run_prompt function")
