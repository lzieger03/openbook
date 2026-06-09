# Frontend-API-Anbindung mit OpenAPI und Svelte

Diese Übersicht ist für den typischen Fall gedacht: Du hast im Django-Backend ein neues Modell oder einen neuen REST-Endpunkt angelegt und willst die Daten jetzt im UI anzeigen oder bearbeiten.

Die wichtigste Idee vorweg: Im Alltag startest du einfach im Projekt-Root `npm start`. Dadurch laufen Django, Frontend-Watcher und die übrigen Entwicklungsdienste. Wenn sich das OpenAPI-Schema ändert, werden die TypeScript-Typen im Frontend automatisch im normalen Build mitgezogen. Falls du das gezielt anstoßen willst, reicht im App-Paket `npm run build:api`.

## 1. Was du im Frontend überhaupt bekommst

Sobald dein Backend-Endpunkt im OpenAPI-Schema auftaucht, erzeugt das Frontend daraus TypeScript-Typen in:

- [src/frontend/app/src/api/openapi/openbook.d.ts](./src/frontend/app/src/api/openapi/openbook.d.ts)
- [src/frontend/app/src/api/openapi/auth.d.ts](./src/frontend/app/src/api/openapi/auth.d.ts)

Diese Typen benutzt du normalerweise nicht direkt aus den generierten Dateien, sondern über [src/frontend/app/src/stores/api.ts](./src/frontend/app/src/stores/api.ts).

Diese Datei hat zwei Aufgaben:

1. Sie exportiert praktische Typ-Aliase wie `openbookSchemas` und `openbookPaths`.
2. Sie gibt dir einen einfachen Wrapper, mit dem du einen konkreten API-Pfad an eine Komponente oder einen Store binden kannst.

Das ist der Grund, warum diese Datei in fast jedem einfachen REST-Beispiel auftaucht: Sie ist die bequeme Einstiegsschicht für den Alltag im Frontend.

## 2. Der normale Ablauf für ein neues Modell im UI

Wenn du ein neues Backend-Modell ins UI bringen willst, ist die Reihenfolge meistens so:

1. Backend fertigstellen.
   Der Endpoint muss im laufenden Django-Server erreichbar sein und im OpenAPI-Schema erscheinen.
2. Frontend-Typen aktualisieren.
   Normalerweise reicht `npm start`. Falls nötig: `cd src/frontend/app && npm run build:api`.
3. Im Frontend entscheiden, wie komplex die Anbindung ist.
   Für einfache Listen/Formulare reicht oft ein direkter API-Zugriff in der Komponente.
   Für komplexere Abläufe lohnt sich ein eigener Store.
4. Die UI-Komponente bauen.
   Dort renderst du nur Daten und reagierst auf Benutzerinteraktionen.

Die eigentliche Entscheidung ist also meistens nur: direkter Wrapper oder eigener Store?

## 3. Einfacher Fall: Komponente spricht direkt mit dem API-Wrapper

Wenn eine Komponente nur einen oder wenige REST-Endpunkte braucht, kannst du direkt den Wrapper aus [src/frontend/app/src/stores/api.ts](./src/frontend/app/src/stores/api.ts) verwenden.

Das Referenzbeispiel dafür ist [src/frontend/app/src/components/app-frame/NavigationBar.svelte](./src/frontend/app/src/components/app-frame/NavigationBar.svelte).

Dort passiert im Kern Folgendes:

1. Die Komponente importiert den Typ des Backend-Objekts.
2. Sie bindet einen konkreten API-Pfad.
3. Sie ruft darauf `GET()`, `POST()`, `PATCH()` oder `DELETE()` auf.

Kleines Beispiel:

```ts
import type { openbookSchemas } from "../../stores/api.js";
import api from "../../stores/api.js";

let items: openbookSchemas["Language"][] = $state([]);

async function loadItems() {
    let backend = await api.openbook("/api/core/languages/", "error-toast");
    let response = await backend.GET();
    items = response.data.results;
}
```

Was hier wichtig ist:

- `openbookSchemas["Language"]` ist der Typ deiner Daten.
- `api.openbook("/api/core/languages/")` bindet den Endpoint.
- `backend.GET()` ist der eigentliche Request.

So würdest du auch ein neues Modell anbinden. Wenn dein Backend zum Beispiel einen Endpoint `/api/library/books/` liefert und dafür ein Schema `Book` erzeugt, sieht das Muster genauso aus:

```ts
import type { openbookSchemas } from "../../stores/api.js";
import api from "../../stores/api.js";

let books: openbookSchemas["Book"][] = $state([]);

async function loadBooks() {
    let backend = await api.openbook("/api/library/books/", "error-toast");
    let response = await backend.GET();
    books = response.data.results;
}
```

Faustregel: Dieses Muster reicht, wenn die Komponente die Daten nur lädt, speichert oder löscht und keine größere eigene Kommunikationslogik braucht.

## 4. Wofür `stores/api.ts` und `api/index.ts` gut sind

An dieser Stelle lohnt sich ein kurzes mentales Modell:

- [src/frontend/app/src/api/index.ts](./src/frontend/app/src/api/index.ts) baut den eigentlichen typisierten Low-Level-Client mit `openapi-fetch`.
- [src/frontend/app/src/stores/api.ts](./src/frontend/app/src/stores/api.ts) macht daraus eine bequemere Alltagsschnittstelle für Komponenten und Stores.

Du arbeitest im normalen Feature-Code fast immer mit [src/frontend/app/src/stores/api.ts](./src/frontend/app/src/stores/api.ts), nicht direkt mit dem Low-Level-Client.

Der Wrapper nimmt dir vor allem drei Dinge ab:

1. Du gibst den Pfad nur einmal an.
2. Du bekommst getypte Methoden wie `GET()` oder `PATCH()`.
3. Fehler können zentral als Toast oder Fehlerseite behandelt werden.

Typisches Muster:

```ts
let backend = await api.openbook("/api/example/items/", "error-toast");

await backend.POST({
    body: {
        name: "Neues Objekt",
    },
});
```

## 5. Komplexer Fall: Eigener Store trennt Logik und UI

Sobald die Kommunikation mehr kann als nur ein einzelnes Laden oder Speichern, wird ein eigener Store meist die bessere Wahl.

Das Referenzbeispiel ist der AI-Chat:

- UI-Komponente: [src/frontend/app/src/components/ai-chat/AiChatPane.svelte](./src/frontend/app/src/components/ai-chat/AiChatPane.svelte)
- Store mit Kommunikationslogik: [src/frontend/app/src/stores/ai-chat.ts](./src/frontend/app/src/stores/ai-chat.ts)

Dort bleibt die Arbeitsteilung sauber:

1. Die Komponente rendert die Oberfläche.
2. Der Store verwaltet Verbindung, Nachrichten und Status.
3. Die Komponente ruft nur noch Methoden des Stores auf.

In der UI sieht das dann sehr schlank aus:

```ts
const aiChat = new AiChatStore();

onMount(() => {
    void aiChat.connect();

    return () => {
        void aiChat.disconnect();
    };
});

await aiChat.sendChatInput("markdown", content);
```

Und der Store kümmert sich um die eigentliche Backend-Kommunikation, hier per WebSocket:

```ts
if (!this.#ws) this.#ws = await api.ws("/ai/chat");
```

Für klassische REST-Features kannst du dasselbe Muster nutzen, auch ohne WebSocket. Ein eigener Store ist sinnvoll, wenn du zum Beispiel:

- Ladezustände und Fehler an einer Stelle bündeln willst,
- mehrere Requests kombinierst,
- Daten vor dem Anzeigen umformst,
- dieselbe Logik in mehreren Komponenten brauchst.

Ein kleines REST-Beispiel für so einen Store könnte so aussehen:

```ts
import type { openbookSchemas } from "../stores/api.js";
import api from "../stores/api.js";
import { ReadableStore } from "../utils/store.js";

type BookState = {
    loading: boolean;
    books: openbookSchemas["Book"][];
};

export class BookStore extends ReadableStore<BookState> {
    constructor() {
        super({ loading: false, books: [] });
    }

    async load() {
        this.update(state => ({ ...state, loading: true }));

        let backend = await api.openbook("/api/library/books/", "error-toast");
        let response = await backend.GET();

        this.update(state => ({
            ...state,
            loading: false,
            books: response.data.results,
        }));
    }
}
```

Die Komponente würde dann nur noch den Store verwenden und keine API-Details mehr kennen.

## 6. Welche Variante du wählen solltest

Nimm direkten Zugriff in der Komponente, wenn:

- es nur um einen kleinen Screen geht,
- ein einzelner Endpoint reicht,
- kaum zusätzliche Logik nötig ist.

Nimm einen eigenen Store, wenn:

- die Komponente sonst zu viel Logik enthalten würde,
- mehrere Backend-Aufrufe zusammengehören,
- Status, Fehler oder Zwischenschritte sauber gekapselt werden sollen,
- das Verhalten wiederverwendbar sein soll.

## 7. Die wichtigsten Beispiele im Projekt

- Direkter REST-Zugriff aus einer Komponente: [src/frontend/app/src/components/app-frame/NavigationBar.svelte](./src/frontend/app/src/components/app-frame/NavigationBar.svelte)
- Bequemer API-Wrapper für den Alltag: [src/frontend/app/src/stores/api.ts](./src/frontend/app/src/stores/api.ts)
- Low-Level-Client mit `openapi-fetch`: [src/frontend/app/src/api/index.ts](./src/frontend/app/src/api/index.ts)
- Entkoppelte Kommunikationslogik in einem Store: [src/frontend/app/src/stores/ai-chat.ts](./src/frontend/app/src/stores/ai-chat.ts)
- UI, die nur noch den Store benutzt: [src/frontend/app/src/components/ai-chat/AiChatPane.svelte](./src/frontend/app/src/components/ai-chat/AiChatPane.svelte)
