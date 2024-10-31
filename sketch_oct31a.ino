#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <time.h>

const char* ssid = "ESP32S";
const char* password = "ESP32SPROJECT";

#define BOTtoken "7375760143:AAGUaVlaVYCb6-Y28QgpT3-0gOIAyd4ISOc"  
#define CHAT_ID "6728605090"

WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);

int botRequestDelay = 1000;
unsigned long lastTimeBotRan;
const int relayPin = 14;
#define DHTPIN 4
#define DHTTYPE DHT22 
DHT dht(DHTPIN, DHTTYPE);

bool isProgramActive = true;  // Set the program to active initially

void setup() {
  Serial.begin(115200);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  dht.begin();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  client.setInsecure();
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println(WiFi.localIP());

  configTime(8 * 3600, 0, "pool.ntp.org");
}

void loop() {
  if (millis() > lastTimeBotRan + botRequestDelay) {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while (numNewMessages) {
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
    lastTimeBotRan = millis();
  }

  if (isProgramActive) {
    float suhu = dht.readTemperature();
    float kelembaban = dht.readHumidity();
    if (isnan(suhu) || isnan(kelembaban)) {
      Serial.println("Gagal membaca sensor DHT!");
      return;
    }
    Serial.print("Suhu: ");
    Serial.print(suhu);
    Serial.print(" C, Kelembaban: ");
    Serial.print(kelembaban);
    Serial.println(" %");

    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
      Serial.println("Gagal mendapatkan waktu!");
      return;
    }

    int currentHour = timeinfo.tm_hour;
    int currentMinute = timeinfo.tm_min;

    if ((suhu >= 30.0 && (currentHour == 9 || currentHour == 16)) || 
        (currentHour == 16 && currentMinute == 10)) {
      digitalWrite(relayPin, HIGH);
    } else {
      digitalWrite(relayPin, LOW);
    }
  }
}

void handleNewMessages(int numNewMessages) {
  for (int i = 0; i < numNewMessages; i++) {
    String chat_id = String(bot.messages[i].chat_id);
    if (chat_id != CHAT_ID) {
      bot.sendMessage(chat_id, "Unauthorized user", "");
      continue;
    }

    String text = bot.messages[i].text;
    String from_name = bot.messages[i].from_name;

    if (text == "/start") {
      String control = "Selamat Datang, " + from_name + ".\n";
      control += "Commands:\n";
      control += "/Status - Cek status relay\n";
      control += "/kondisisuhu - Cek suhu\n";
      control += "/startProgram - Aktifkan program\n";
      control += "/stopProgram - Nonaktifkan program\n";
      bot.sendMessage(chat_id, control, "");
    }

    if (text == "/Status") {
      String status = (digitalRead(relayPin) == HIGH) ? "Relay Nyala (Penyiraman Aktif)" : "Relay Mati (Penyiraman Nonaktif)";
      bot.sendMessage(chat_id, status, " ");
    }

    if (text == "/kondisisuhu") {
      float suhu = dht.readTemperature();
      if (!isnan(suhu)) {
        bot.sendMessage(chat_id, "Suhu saat ini: " + String(suhu) + "°C", "");
      } else {
        bot.sendMessage(chat_id, "Gagal membaca suhu.", "");
      }
    }

    if (text == "/startProgram") {
      isProgramActive = true;
      bot.sendMessage(chat_id, "Program diaktifkan. Kondisi otomatis aktif.", "");
    }

    if (text == "/stopProgram") {
      isProgramActive = false;
      digitalWrite(relayPin, LOW);  // Matikan relay saat program nonaktif
      bot.sendMessage(chat_id, "Program dinonaktifkan. Relay dalam keadaan mati.", "");
    }
  }
}

