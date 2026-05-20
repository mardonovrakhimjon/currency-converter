import requests


def get_live_rates():
    """Markaziy bank va Milliy bankdan real vaqtdagi kurslarni avtomatik olish"""
    cbu_url = "https://cbu.uz"
    nbu_url = "https://nbu.uz"

    data = {"CBU": {}, "NBU": {}}

    try:
        # 1. Markaziy bank kurslarini olish
        cbu_res = requests.get(cbu_url, timeout=5).json()
        for item in cbu_res:
            if item["Ccy"] in ["USD", "EUR", "RUB"]:
                data["CBU"][item["Ccy"]] = float(item["Rate"])

        # 2. Milliy Bank (NBU) real kurslarini olish (Sotish va Sotib olish)
        nbu_res = requests.get(nbu_url, timeout=5).json()
        for item in nbu_res:
            if item["code"] in ["USD", "EUR", "RUB"]:
                data["NBU"][item["code"]] = {
                    # Agar bank saytida kurs bo'lmasa, rasmiy kursni qo'yadi
                    "buy": float(item["cb_price"] if not item["nbu_buy_price"] else item["nbu_buy_price"]),
                    "sell": float(item["cb_price"] if not item["nbu_cell_price"] else item["nbu_cell_price"]),
                }
    except Exception as e:
        print(
            "Internetdan ma'lumot olishda xato bo'ldi. Internetni tekshiring."
        )

    return data


def main():
    print("Kurslar internetdan yuklanmoqda, kuting...")
    live_data = get_live_rates()

    currency_code = input("\nValyuta kodini kiriting (USD, EUR, RUB): ").upper()
    if currency_code not in ["USD", "EUR", "RUB"]:
        print("Noto‘g‘ri valyuta kodi.")
        return

    action = input(
        "Siz valyutani bankka sotasizmi (1) yoki bankdan sotib olasizmi (2)? "
    )
    amount = float(input("Miqdorni kiriting: "))

    # Markaziy bank kursi
    cbu_rate = live_data["CBU"].get(currency_code)
    print("\n" + "=" * 60)
    if cbu_rate:
        print(f"Markaziy Bank rasmiy kursi: 1 {currency_code} = {cbu_rate:,.2f} UZS")
    print("=" * 60)

    # NBU kursi (Internetdan kelgan jonli ma'lumot)
    nbu_currency = live_data["NBU"].get(currency_code)
    if nbu_currency:
        rate_type = "buy" if action == "1" else "sell"
        current_rate = nbu_currency[rate_type]
        total_sum = amount * current_rate

        action_text = "Sotish" if action == "1" else "Sotib olish"
        print(f"\nMilliy Bank (NBU) JONLI kursi ({action_text}):")
        print(f"1 {currency_code} = {current_rate:,.2f} UZS")
        print(f"Siz uchun yakuniy summa: {total_sum:,.2f} UZS")
    else:
        print("\nTijorat bankidan ma'lumot olib bo'lmadi.")


main()
