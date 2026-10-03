from dotenv import load_dotenv
load_dotenv()

from langfuse import get_client

langfuse = get_client()

with langfuse.start_as_current_observation(
    as_type="span",
    name="teste-conexao",
    input={"mensagem": "olá, Langfuse"},
) as span:
    span.update(output={"resultado": "funcionou"})

langfuse.flush()
print("Enviado! Confira em http://localhost:3000")