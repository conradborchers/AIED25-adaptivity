def formatStringList(stringOrStringList: str | list[str]) -> list[str]:
    if isinstance(stringOrStringList, list):
        return stringOrStringList
    elif not stringOrStringList:
        return []
    elif stringOrStringList == "character(0)":
        return []
    else:
        return [stringOrStringList]
