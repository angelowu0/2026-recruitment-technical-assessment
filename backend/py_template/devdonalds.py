from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = None

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	"""
	parses recipeName in accordance to requirements listed out in readme:
	- all hyphens '-' and underlines '_' are replaced with whitespace ' '
	- all characters must be alphabetical or whitespace
	- no leading, trailing or multiple whitespaces
	- every word must have its first character capitalised and other letters
	  in lower case
	- must have > 0 characters once parsed

	:param recipeName: string of the recipe name
	:return: None if parsed string is empty, the parsed string otherwise
	"""

	# Replaces '-' and '_' with whitespace
	parsed_recipe_name = recipeName.translate(str.maketrans("-_", "  "))

	# Removes multiple, leading and trailing whitespaces
	parsed_recipe_name = " ".join(parsed_recipe_name.split())

	# Removes all non-alphabetical/whitespace characters
	regex = re.compile("[^a-zA-Z ]")
	parsed_recipe_name = regex.sub("", parsed_recipe_name)

	# Capitalises the first letter of each word, and makes every other letter lower case
	parsed_recipe_name = parsed_recipe_name.title()

	if len(parsed_recipe_name) == 0:
		return None

	return recipeName


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	"""
	Endpoint for create_entry, calls add_entry to validate and add to cookbook

	"""
	try:
		data = request.get_json()
		entry_type = data.get("type", "")
		name = data.get("name", "")
		required_items = data.get("requiredItems", "")

		cook_time = data.get("cookTime", "")

		add_entry(entry_type, name, required_items, cook_time)

		return jsonify({}), 200

	except ValueError as e:
		return str(e), 400



def add_entry(entry_type: str, name: str, required_items: List[Dict[str, Union[str, int]]], cook_time: str) -> None:
	"""
	Validates and adds an entry to the cookbook

	:param entry_type: string for the type of entry it is
	:param name: name of the entry
	:param required_items: the items required for entry, given as a list of dictionaries
	:param cook_time: string for the time it takes to cook, as if entry is recipe, may be empty string
	:return: string of error message (or NO_ERROR, ('')) if none)
	"""
	valid_entry(entry_type, name, required_items, cook_time)

	if entry_type == "recipe":
		print(required_items, "HEREEEEEE", flush=True)

		required_items_list = [RequiredItem(item["name"], item["quantity"]) for item in required_items]
		cookbook.append(Recipe(name, required_items_list))

	if entry_type == "ingredient":
		cookbook.append(Ingredient(name, int(cook_time)))


def valid_entry(entry_type: str, name: str, required_items: List[Dict[str, Union[str, int]]], cook_time: str) -> None:
	"""
	Validates if an entry is valid

	:param entry_type: type of entry
	:param name: name of entry
	:param required_items: list of dictionaries of entry
	:param cook_time: string for time to cook
	:return:Error message
	"""
	if entry_type == "recipe" and not no_duplicate_names_in_required_items(required_items):
		raise ValueError("Invalid Required Items: Duplicate Names in Required Items")

	elif entry_type == "ingredient" and int(cook_time) < 0:
		raise ValueError("Invalid Cook Time: Cook Time Less Than 0")

	elif entry_type not in ("recipe", "ingredient"):
		raise ValueError("Invalid Type: Type Must Be Recipe or Ingredient")

	# Checks if a name already exists in the cookbook
	elif any(entry.name == name for entry in cookbook):
		raise ValueError("Invalid Name: Name Already Exists")


def no_duplicate_names_in_required_items(required_items: List[Dict[str, Union[str, int]]]) -> bool:
	"""
	Checks if required items has two items with the same name
	:param required_items: List of dictionaries which represent the items
	:return: Boolean for whether duplicates exist
	"""
	unique_items = set()

	# Adds items into unique_items set until either reaches end, or finds item already in the set
	for i in required_items:
		if i["name"] not in unique_items:
			unique_items.add(i["name"])

		else:
			return False

	return True


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	try:
		name = request.args.get("name")
		recipe_summary = create_summary(name)

		return jsonify(recipe_summary), 200
	except ValueError as e:
		return str(e), 400
	except KeyError as e:

		return str(e), 400


def create_summary(name: str) -> Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]:
	"""
	Creates a summary for a recipe
	:param name: Name of recipe
	:return: Summary in format given in readme
	"""
	entry = find_cookbook_entry(name)

	if type(entry) == Ingredient:
		raise ValueError("Invalid Name: Name refers to an Ingredient")

	recipe_summary = do_recipe_simplify(entry, 1)

	return {
		'name': name,
		'cook_time': recipe_summary["cook_time"],
		'ingredients': [
			{'name': item,
			 'quantity': recipe_summary["ingredients"][item]} for item in recipe_summary["ingredients"]
		]
	}


def do_recipe_simplify(entry: CookbookEntry, quantity: int) -> Dict[str, Union[int, Dict[str, int]]]:
	"""
	Recursively simplifies a recipe into its ingredients
	:param entry: CookbookEntry of any type
	:param quantity: Quantity of entry's base ingredients to be multiplied by
	:return: name, cook time and ingredients dictionary
	"""

	# Base case, entry is an ingredient
	if type(entry) == Ingredient:
		cookbook_entry = find_cookbook_entry(entry.name)

		if type(cookbook_entry) != Ingredient:
			raise TypeError(f"Invalid Type: Expected Type Ingredient but got {type(cookbook_entry)}")

		return {
			'cook_time': getattr(cookbook_entry, "cook_time") * quantity,
			'ingredients': {cookbook_entry.name: quantity}
		}

	ingredients: Dict[str, int] = {}
	cook_time = 0

	# Goes through every item in entry's required items and adds its ingredients and cooktime
	for item in getattr(entry, "required_items"):
		cookbook_entry = find_cookbook_entry(item.name)
		temp_summary = do_recipe_simplify(cookbook_entry, item.quantity)
		cook_time += temp_summary["cook_time"]
		combine_required_item_dicts(ingredients, temp_summary["ingredients"])

	return {
		'cook_time': cook_time * quantity,
		'ingredients': {ingredient: ingredients[ingredient] * quantity for ingredient in ingredients}
	}

def combine_required_item_dicts(dict_a: Dict[str, int], dict_b: Dict[str, int]) -> None:
	"""
	Combines dict a and b into dict a
	:param dict_a: first dict
	:param dict_b: second dict
	"""
	for item in dict_b:
		dict_a[item] = dict_a.get(item, 0) + dict_b[item]


def find_cookbook_entry(name: str) -> CookbookEntry:
	"""
	Finds a cookbook entry given its name
	:param name: string of the cookbook entry name
	:return: CookBookEntry corresponding to name
	"""
	for entry in cookbook:
		if getattr(entry, "name") == name:
			return entry
	raise KeyError("Invalid Name, No Entry With Name {name}")


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
