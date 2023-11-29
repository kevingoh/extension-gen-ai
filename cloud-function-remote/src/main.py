import vertexai
import functions_framework
import logging
from flask import jsonify
from vertexai.preview.language_models import TextGenerationModel


LOCATION = "us-central1"  # @param {type:"string"}

vertexai.init(location=LOCATION)

# Max INT64 value encoded as a number in JSON by TO_JSON_STRING. Larger values are encoded as
# strings.
# See https://cloud.google.com/bigquery/docs/reference/standard-sql/json_functions#json_encodings

@functions_framework.http
def bq_vertex_remote(request):
  try:
    return_value = []
    request_json = request.get_json()
    calls = request_json['calls']
    
    vertex_model = TextGenerationModel.from_pretrained("text-bison-32k")
    # vertex_model = TextGenerationModel.get_tuned_model('projects/XXXXXX/locations/us-central1/models/XXXXXXXXXXXXXX')    
    for call in calls:
      if call is not None and len(call) == 1:
        prompt = call[0]
        logging.info("Prompt: " + prompt)        
        if(isinstance(prompt, str)):
          genai_return = tuned_model.predict(
            prompt=prompt,
            temperature= 0.2,
            max_output_tokens= 256,
            top_p= 0.8,
            top_k= 40
            )
          return_value.append(genai_return.text)
        else:
            #   error, receiving more 
            logging.error("Receiving more than one element or null")
            return_value.append(None)

    replies = [str(x) for x in return_value]
    return jsonify( { "replies" :  replies } )
  except Exception as e:
    return jsonify( { "errorMessage": str(e) } ), 400  

          
            
          

