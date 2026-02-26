
def validated(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        presence_set = set()
        for v in result.values():
            pins = v.get('pins',{}).values()
            is_simulated = v.get('simulated',True)
            if not is_simulated and len(pins) == 0:
                raise ValueError("You have not specified some pins")

            for pin in pins:
                if isinstance(pin,int):
                    if pin in presence_set:
                        raise ValueError("Some pins repeat in your config")
                    presence_set.add(pin)
                if isinstance(pin,list):
                    for p in pin:
                        if p in presence_set:
                            raise ValueError("Some pins repeat in your config")
                        presence_set.add(p)
        return result
    return wrapper
