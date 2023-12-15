class ACCTest:

    def __init__(self, id, ref_img, test_img, prompt):
        self.id = id
        self.ref_img = ref_img.strip()
        self.test_img = test_img.strip()
        self.prompt = prompt
        self.num_questions = 3
        self.result_q1 = -1
        self.result_q2 = -1
        self.result_q3 = -1

    def __str__(self):
        return self.id + "," + self.prompt + "," + str(self.result_q1) + "," + str(self.result_q2) + "," + str(self.result_q3)

    def get_button_labels(self, number):
        return ["Yes", "No", "Partial"]

    def get_ref_image(self, number):
        return self.ref_img

    def get_test_img(self, number):
        return self.test_img

    def get_question(self, number):
        if number == 1:
            return "Q1: Does the relevancy map highlight a " + self.prompt + "?"
        if number == 2:
            return "Q2: Does the relevancy map miss a " + self.prompt + "?"
        if number == 3:
            return "Q3: Does the relevancy map highlight anything that isn't a " + self.prompt + "?"

    def get_choice(self, number):
        if number == 1:
            return "You chose " + str(self.result_q1)
        if number == 2:
            return "You chose " + str(self.result_q2)
        if number == 3:
            return "You chose " + str(self.result_q3)

    def get_result(self, number):
        if number == 1:
            return self.result_q1
        if number == 2:
            return self.result_q2
        if number == 3:
            return self.result_q3

    def save_result(self, result, number):
        if number == 1:
            self.result_q1 = result
        if number == 2:
            self.result_q2 = result
        if number == 3:
            self.result_q3 = result

