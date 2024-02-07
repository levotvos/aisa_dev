# Annotációt Is Segítő Alkalmazás

## Architektúra

```
                     +--------------------+       +---------------+      +---------------+
                     |                    |       |               |      |               |
                     |  Fine-tuning with  |<------+ Training Data |<-----+  LabelStudio  |
                     |       LoRA         |       | Converter     |      |  Annotations  |
                     |                    |       |               |      |  Validated    |
                     +----------+---------+       +---------------+      +-------^-------+
                                |                                                |
                  +-------------+------------------------------------+           |
                  |             |                FastAPI & Streamlit |           |
                  |             v                                    |           |
                  |  +--------------------+                          |   +-------+-------+
                  |  |                    |                          |   |               |
                  |  |   Language Model   |                          |   |  Human Annot. |
                  |  |                    |                          |   |               |
                  |  +--------------------+                          |   +-------^-------+
                  |   mistralai_mistral-7b-instruct-v0.2             |           |
                  |             |                                    |           |
                  |             |                                    |           |
+------------+    |  +----------v---------+     +-----------------+  |   +-------+-------+
|            |    |  |                    |     |                 |  |   |               |
|  Text      +----+->|      Llama.cpp     +---->| [Output Parser] +--+-->|  LabelStudio  |
|  Document  |    |  | (llama-cpp-python) |     |                 |  |   |  Annotations  |
|            |    |  |                    |     |                 |  |   |  Predictions  |
+------------+    |  +--------------------+     +-----------------+  |   +---------------+
                  |                                                  |
                  +--------------------------------------------------+
```

### Llama.cpp

A Llama.cpp lehetővé teszi, hogy (akár kvantált) generatív nagy nyelvi modelleket futtassuk változatos hardverek felett, egyszerű rendszereken is. A pusztán C/C++-ban írt könyvtárat Python-os keretbe a llama-cpp-python könyvtár ágyazza.
Az AISA szoftver esetében a Llama.cpp segítségével valósítjuk meg, hogy a használt nyelvi modellek fussanak kizárólag CPU-n is, korlátozott memória használattal.

Licensz: MIT
További információ: https://github.com/ggerganov/llama.cpp

### Mistral

Az AISA szoftver részben egy kísérlet arra irányulóan, hogy miként lehet egy hatékony, különböző célterületekre rendkívül jól adaptálható és alacsony erőforrás igényű automatikus szövegfeldolgozó alkalmazást készíteni. Ehhez kézenfekvőnek tűnik egy "state-of-the-art" nagy nyelvi modell (LLM) alkalmazása. 

Licensz: Apache 2.0
További információ: https://mistral.ai/product/

### FastAPI

A FastAPI egy modern alkalmazásprogramozási felületek kialakítására szolgáló keretrendszer. Segítségével egy olyan szoftverarchitektúrát valósíthatunk meg, ahol a szoftver funkciói könnyedén elérhetőek elosztott rendszerek esetében is. Ez lehetővé teszi, hogy AISA szoftver magját összekapcsoljuk ráépülő alkalmazásokkal, mint például egy webes felhasználói felülettel vagy egy külön adatbázis kapcsolatot létesítő szkripttel, és mindemellett, hogy a funkciók egyszerre aszinkron akár több kliens által is használhatóak, nagyban skálázhatóak legyenek.

Licensz: MIT
További információ: https://fastapi.tiangolo.com/
