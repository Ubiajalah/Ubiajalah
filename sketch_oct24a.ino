#include <DHT.h>

// Pin konfigurasi
#define DHTPIN 2         // Pin sensor DHT22 terhubung ke GPIO 12
#define DHTTYPE DHT22     // Menggunakan sensor DHT22
#define RELAYPIN 12      // Pin relay terhubung ke GPIO 5

DHT dht(DHTPIN, DHTTYPE);

// Variabel
int suhu;
int ambangSuhu = 30;      // Ambang suhu untuk menyalakan pompa

void setup() {
  // Inisialisasi Serial Monitor
  Serial.begin(115200);
  
  // Inisialisasi DHT Sensor
  dht.begin();

  // Inisialisasi Relay
  pinMode(RELAYPIN, OUTPUT);
  digitalWrite(RELAYPIN, LOW);  // Matikan relay di awal
}

void loop() {
  // Membaca suhu dari sensor
  suhu = dht.readTemperature();

  // Menampilkan suhu di Serial Monitor
  Serial.print("Suhu:30 ");
  Serial.print(suhu);
  Serial.println("30 °C");

  // Logika kontrol penyiraman
  if (suhu >= ambangSuhu) {
    digitalWrite(RELAYPIN, HIGH);  // Nyalakan pompa jika suhu tinggi
    Serial.println("Pompa Menyala (Suhu tinggi)");
  } else {
    digitalWrite(RELAYPIN, LOW);   // Matikan pompa jika suhu rendah
    Serial.println("Pompa Mati (Suhu rendah)");
  }

  delay(2000);  // Tunggu 2 detik sebelum loop ulang
}

