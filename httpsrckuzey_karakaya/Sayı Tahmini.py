import time

def sayi_bulma_oyunu():
    print("\n=== SAYI BULMA OYUNU ===")
    print("Aklından bir sayı tut, ben bulayım 😎")

    ust = int(input("Üst sınırı gir (örnek 100): "))
    alt = 0
    deneme = 0

    print(f"\n{alt} ile {ust} arasında bir sayı tuttun.")
    print("Cevap olarak: yukarı / aşağı / bildin yaz\n")

    baslangic = time.time()

    while True:
        if alt > ust:
            print("❌ Cevapların çelişiyor, oyunu bozma 😄")
            break

        tahmin = (alt + ust) // 2
        deneme += 1
        print(f"Tahminim: {tahmin}")

        cevap = input("Cevap ne? (yukarı/aşağı/bildin): ").lower()

        if cevap == "bildin":
            sure = time.time() - baslangic
            print("\n🎉 SAYIYI BULDUM!")
            print(f"🔢 Deneme sayısı: {deneme}")
            print(f"⏱️ Süre: {sure:.2f} saniye")

            if deneme <= 7:
                print("🧠 Seviye: Süper Zeka")
            elif deneme <= 10:
                print("👍 Seviye: İyi")
            else:
                print("🙂 Seviye: Geliştirilebilir")
            break

        elif cevap == "yukarı":
            alt = tahmin + 1
        elif cevap == "aşağı":
            ust = tahmin - 1
        else:
            print("⚠️ Lütfen sadece yukarı, aşağı veya bildin yaz!")

def main():
    while True:
        sayi_bulma_oyunu()
        tekrar = input("\nTekrar oynamak ister misin? (e/h): ").lower()
        if tekrar != "e":
            print("👋 Görüşürüz!")
            break

main()
