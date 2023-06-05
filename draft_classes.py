from datetime import datetime
from dataclasses import dataclass


@dataclass
class RecipesTimer:
    prepearing_minutes: int = 0
    cooking_minutes: int = 0

    def repr_prepearing():
        if self.prepearing_minutes >= 60:
            hours = self.prepearing_minutes // 60
            minutes = self.prepearing_minutes % 60
            return f"{hours} ч., {minutes} мин."
        return f"{self.prepearing_minutes} мин."

    def repr_cooking():
        if self.cooking_minutes >= 60:
            hours = self.cooking_minutes // 60
            minutes = self.cooking_minutes % 60
            return f"{hours} ч., {minutes} мин."
        return f"{self.cooking_minutes} мин."


class User:
    def __init__(self, name: str = "", email: str = "", password: str = ""):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<Пользователь: {self.name}, {self.email}>"


class Colour:
    def __init__(self, name, colour):
        self._check_colour(colour)
        self.name = name
        self.RGB = tuple(colour)

    def _check_colour(self, colour):
        if len(colour) != 3:
            raise ValueError(f"Некорректное значение цвета: {colour}")
        for c in colour:
            if not isinstance(c, int) or c < 0 or c > 255:
                raise ValueError(
                    f"Некорректное значение компонента {c} для цвета {colour}"
                )

    def __repr__(self):
        return f"<Цвет: {self.name} {self.RGB}>"


class ProductCategory:
    def __init__(self, name: str, colour: Colour):
        self.name = name
        self.colour = colour

    def __repr__(self):
        return f"<Категория: {self.name}>"


class Product:
    def __init__(self, name: str, category: ProductCategory):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"<Продукт: {self.name}>"


class MeasurementUnit:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Единица измерения: {self.name}>"


class Ingredient:
    def __init__(self, product: Product, quantity: int | float, unit: MeasurementUnit):
        self._check_quantity(quantity)
        self.product = product
        self.quantity = quantity
        self.unit = unit

    def _check_quantity(self, quantity):
        if quantity <= 0:
            raise ValueError(
                f"Количество ингредиента не может быть меньше 0 ({quantity})"
            )

    def __eq__(self, other):
        return self.product == other.product and self.unit == other.unit

    def __add__(self, other):
        return ShippingListItems(
            self.product, self.quantity + other.quantity, self.unit
        )

    def __repr__(self):
        return f"<Ингредиент: {self.product.name}, {self.quantity} {self.unit.name}>"


class RecipeCategory:
    def __init__(self, name: str, colour: Colour):
        self.name = name
        self.colour = colour

    def __repr__(self):
        return f"<Категория рецептов: {self.name}>"


class Recipe:
    def __init__(
        self,
        user: User,
        name: str,
        recipe_category: RecipeCategory,
        description: str,
        ingredients: list[Ingredient],
        timer: RecipesTimer,
    ):
        self.master = user
        self.name = name
        self.category = recipe_category
        self.description = description
        self.timer = timer
        self.ingredients = ingredients
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __repr__(self):
        return f"<Рецепт: {self.name}>"


class ShoppingList:
    def __init__(self, user: User, name=""):
        self.master = user
        self.name = name
        self.items = []
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def add(self, smth_to_add):
        if isinstance(smth_to_add, Recipe):
            self._add_from_recipe(smth_to_add)
        if isinstance(smth_to_add, Ingredient):
            self._add_item(smth_to_add)

    def _add_item(self, item: Ingredient):
        try:
            index = self.items.index(item)
            self.items[index] += item
        except ValueError:
            self.items.append(item)

    def _add_from_recipe(self, recipe: Recipe):
        for ingredient in recipe.ingredients:
            self._add_item(ingredient)

    def __repr__(self):
        return f"<Список покупок: {self.name}, в составе: {', '.join(map(str, self.items))}>"


if __name__ == "__main__":
    test_user = User("Тимофей", "tim@test.ch", "12345678")
    print(test_user)

    gr = MeasurementUnit("грамм")
    th = MeasurementUnit("шт.")
    print(gr, th)

    white = Colour("белый", [255, 255, 255])
    yellow = Colour("желтый", [255, 255, 0])
    print(white, yellow)

    from_animals = ProductCategory("животного происхождения", white)
    print(from_animals)

    eggs = Product("яйцо", from_animals)
    sausage = Product("сосиски", from_animals)
    print(eggs, sausage)

    list_to_ship = ShoppingList(test_user, "на недельку")
    few_sausages = Ingredient(sausage, 12, th)
    list_to_ship.add(few_sausages)
    print(list_to_ship)

    time_to_result = RecipesTimer(1, 5)
    print(time_to_result)

    breakfast = RecipeCategory("завтрак", yellow)
    print(breakfast)

    description = (
        "нарезать сосиски, выложить на сковородку, залить яйцами, жарить до готовности"
    )
    first_ingredient = Ingredient(eggs, 2, th)
    second_ingredient = Ingredient(sausage, 100, gr)
    print(first_ingredient, second_ingredient)

    eggs_and_sausage = Recipe(
        test_user,
        "яичница",
        breakfast,
        description,
        ingredients=[first_ingredient, second_ingredient],
        timer=time_to_result,
    )
    print(eggs_and_sausage)

    list_to_ship.add(eggs_and_sausage)
    print(list_to_ship)
