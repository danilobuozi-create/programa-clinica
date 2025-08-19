\
    import re
    from datetime import datetime, date

    def cpf_format(cpf: str) -> str:
        if not cpf: return ""
        nums = re.sub(r"\\D", "", cpf)
        if len(nums) == 11:
            return f"{nums[0:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:11]}"
        return cpf or ""

    def telefone_format(tel: str) -> str:
        if not tel: return ""
        nums = re.sub(r"\\D", "", tel)
        if len(nums) == 11: return f"({nums[0:2]}) {nums[2:7]}-{nums[7:11]}"
        if len(nums) == 10: return f"({nums[0:2]}) {nums[2:6]}-{nums[6:10]}"
        return tel or ""

    def currency(v) -> str:
        if v is None: return ""
        try: v = float(v)
        except: return str(v)
        s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {s}"

    def date(v, fmt="%d/%m/%Y"):
        if v is None: return ""
        if isinstance(v, (datetime, date)): return v.strftime(fmt)
        try: return datetime.fromisoformat(str(v)).strftime(fmt)
        except: return str(v)

    def idade(nasc: str) -> str:
        try:
            d = datetime.fromisoformat(nasc).date(); today = date.today()
            years = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
            return str(years)
        except: return ""
