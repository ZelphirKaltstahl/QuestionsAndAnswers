from decimal import Decimal, localcontext, ROUND_DOWN

def truncate_number(number, places):
	if not isinstance(places, int):
		raise ValueError("Decimal places must be an integer.")
	if places < 1:
		raise ValueError("Decimal places must be at least 1.")

	with localcontext() as context:
		context.rounding = ROUND_DOWN
		exponent = Decimal(str(10 ** -places))

	return Decimal(str(number)).quantize(exponent).to_eng_string()