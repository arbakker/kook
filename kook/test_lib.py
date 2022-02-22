from kook.lib import ocr_image, ocr_image_front, get_recipe_steps,get_all_ingredients,get_titles,SCAN_DIR
import json

class TestClass:
    back_text = ""
    front_text = ""

    def test_ocr_image(self):
        # images=("2022-02-21 13.59.21.jpg", "2022-02-21 14.01.36.jpg")
        # images=("2022-02-21 22.05.33.jpg", "2022-02-21 22.06.25.jpg")
        # images=("2022-02-21 22.00.49.jpg","2022-02-21 22.01.20.jpg")
        # images=("2022-02-21 21.57.56.jpg","2022-02-21 21.58.26.jpg")
        # images=("2022-02-19 17.38.34.jpg", "2022-02-19 17.38.59.jpg")
        # images=("2022-02-20 13.12.43.jpg", "2022-02-20 13.13.14.jpg")
        # images=("2022-02-21 22.00.49.jpg","2022-02-21 22.01.20.jpg")
        # images=("2022-02-20 11.59.05.jpg", "2022-02-20 12.00.07.jpg")
        images=("2022-02-22 10.56.29.jpg","2022-02-22 10.57.03.jpg")
        self.__class__.front_text = ocr_image_front(f"{SCAN_DIR}/{images[0]}")
        self.__class__.back_text = ocr_image(f"{SCAN_DIR}/{images[1]}")
        print(self.front_text)
        assert self.front_text is not "" 
        assert self.back_text is not "" 

    def test_get_recipe_steps(self):
        steps = get_recipe_steps(self.back_text)
        assert len(steps) == 6
        assert "Je kunt je in je online account" not in steps[5]
    
    def test_get_all_ingredients(self):
        ingredients = get_all_ingredients(self.back_text)
        print(json.dumps(ingredients,indent=4))
        assert len(ingredients) == 12

    def test_get_titles(self):
        title,subtitle,description,slug = get_titles(self.front_text)
        assert title == "Penne in saus van gehakt en vijgen"
        assert subtitle == "met cherrytomaten en bieslook"
        assert description.startswith("Pasta met gehaktsaus?")

