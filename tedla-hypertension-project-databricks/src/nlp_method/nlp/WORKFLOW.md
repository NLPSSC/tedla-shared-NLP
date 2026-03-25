# NLPWorker.__call__ Workflow Diagram

This diagram illustrates the workflow path taken when the `__call__` method is invoked on an `NLPWorker` instance, including the call to `NLPProcessor.__call__` and note processing with MedSpaCy.

```mermaid
flowchart TD
    A["NLPWorker.__call__ invoked"] --> B["Worker signals ready"]
    B --> C["Enter processing loop"]
    C --> D["Queue get: notes_df"]
    D --> E{"notes_df is None?"}
    E -- Yes --> F["Set _complete True"]
    F --> G["Log completion"]
    G --> H["Exit loop"]
    E -- No --> I["Update totals"]
    I --> J["Start metrics cycle clock"]
    J --> K["Call nlp processor (notes_df)"]
    K --> L["NLPProcessor.__call__"]
    L --> M["Process notes with MedSpaCy"]
    M --> N["Yield processed docs"]
    N --> C
    D --> O["Exception: Empty"]
    O --> C
    D --> P["Exception: Other"]
    P --> Q["Log error & raise"]
    Q --> H
```
