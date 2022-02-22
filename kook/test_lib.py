from kook.lib import ocr_image, ocr_image_front, get_recipe_steps,get_all_ingredients,get_titles,get_project_kook
import json

class TestClass:
    back_text = ""
    front_text = ""

    def test_ocr_image(self):
        proj_kook_dir = get_project_kook()
        images=(f"{proj_kook_dir}/test-data/2022-02-21 13.59.21.jpg",
            f"{proj_kook_dir}/test-data/2022-02-21 14.01.36.jpg"
        )
        self.__class__.front_text = ocr_image_front(f"{images[0]}")
        self.__class__.back_text = ocr_image(f"{images[1]}")
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

