import json
from flask import Flask, request
import openai


class GptApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.openai_api_key = "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"
        self.model_engine = "text-davinci-003"
        self.prompt_history = {}

        openai.api_key = self.openai_api_key

        self.app.add_url_rule('/profile-review', view_func=self.profile_review, methods=['POST'])
        self.app.add_url_rule('/essay', view_func=self.essay, methods=['POST'])
        self.app.add_url_rule('/suggestions', view_func=self.suggestions, methods=['POST'])
        self.app.add_url_rule('/history', view_func=self.history, methods=['GET'])

    def run(self):
        self.app.run(debug=True)

    def profile_review(self):
        profile_data_str = request.data.decode('utf-8')
        profile_data = json.loads(profile_data_str)

        prompt = f"Can you make sense of the following profile data and tell me if I am a strong candidate for " \
                 f"{', '.join(profile_data['target_schools'])}? {profile_data['profile_data']}"

        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            temperature=0.7,
            max_tokens=40,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        text = response["choices"][0].get("text", "")
        response_data = {'text': text}

        self.prompt_history["profile_review"] = text

        return json.dumps(response_data)

    def essay(self):
        request_data_str = request.data.decode('utf-8')
        constraints = json.loads(request_data_str)
        prompt = f"give me an essay that I can submit along with my application to the business schools based on my " \
                 f"profile with the following condition: {constraints['constraints']}"

        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            temperature=0.9,
            max_tokens=40,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        text = response["choices"][0].get("text", "")
        response_data = {'text': text}

        self.prompt_history["essay"] = text

        return json.dumps(response_data)

    def suggestions(self):
        query_data_str = request.data.decode('utf-8')
        query_data = json.loads(query_data_str)
        prompt = f"Give me suggestions on how I can improve my profile to increase my chances of getting an admit from" \
                 f"my target business schools, {query_data['query']}  also tell me based on your " \
                 f"analysis which mba programs from my target schools will have the course curriculum that best " \
                 f"aligns with my professional work experience, here's your analysis " \
                 f"for reference: {self.prompt_history['profile_review']}"

        response = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            temperature=0.9,
            max_tokens=40,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        text = response["choices"][0].get("text", "")
        response_data = {'text': text}

        self.prompt_history["suggestions"] = text

        return json.dumps(response_data)

    def history(self):
        return json.dumps(self.prompt_history)


if __name__ == '__main__':
    gpt_app = GptApp()
    gpt_app.run()
