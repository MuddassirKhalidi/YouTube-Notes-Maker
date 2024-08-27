import openai

class NotesMaker:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model

    def write_to_file(self, text, output_filename="notes.txt"):
        with open(output_filename, 'a') as file:
            file.write(text)

    def generate_notes(self, text):
        response = openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert Notes Maker. You are given large corpuses of lectures transcribed to text to analyze, extract valuable insights and make notes which allow students to understand the text without having to go through it themselves."},
                {"role": "user", "content": text}
            ]
        )
        notes = response.choices[0].message.content
        self.write_to_file(notes)