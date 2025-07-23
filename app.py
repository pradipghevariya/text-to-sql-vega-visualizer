import os
import json
import pandas as pd
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import numpy as np

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "<your-gemini-api-key>"


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=1024
)

df = pd.DataFrame({
    'Product': ['Product A'] * 5 + ['Product B'] * 5,
    'Month': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05'] * 2,
    'Sales': [200, 250, 225, 275, 300,    # Sales for Product A
              150, 160, 155, 165, 170],   # Sales for Product B
    # For the first month, no MoM change is available (NaN); subsequent values are pre‐computed percentages
    'MoM_Change (%)': [np.nan, 25.0, -10.0, 22.22, 9.09,
                       np.nan, 6.67, -3.13, 6.45, 3.03]
})


def get_dataframe_schema(df):
    return {
        "columns": dict(df.dtypes.apply(lambda x: x.name)),
        "sample_data": df.head(2).to_dict(orient="list")
    }


template = '''
You are a deterministic data visualization assistant with expertise in Vega‑Lite v5. You must generate a complete, syntactically correct, and schema‑compliant Vega‑Lite JSON specification based on the official JSON schema defined at https://vega.github.io/schema/vega-lite/v5.json. Do not output any extra commentary or text—only valid JSON.

User Question: {question}

DataFrame Schema:
- Columns (with data types): 
    {columns}
    
- Sample Data: 
    {sample_data}

Instructions:
    - Only include keys defined in the schema (such as "mark", "encoding", "transform", "title", "config", etc.) and use proper data types.


1. **Mark Property:**  
   - The "mark" property must be one of the allowed values defined in the schema. Allowed mark types are:
       "arc", "area", "bar", "image", "line", "point", "rect", "rule", "text", "tick", "trail", "circle", "square", "geoshape"
   - You may specify additional mark properties (like "color", "fill", "stroke", "opacity", etc.) if relevant.

2. **Encoding Property:**  
   - The "encoding" property must include at least the "x" and "y" channels.
   - For each channel, include:
       - "field": a valid column name from the DataFrame.
       - "type": one of "quantitative", "temporal", "ordinal", or "nominal".
   - Optionally, add additional channels (such as "color", "size", "tooltip", "detail", "shape") as needed to answer the question.

3. **Transformations and Additional Properties (Optional):**  
   - If the user question requires data manipulation, include a "transform" array with objects using keys like "filter", "calculate", "aggregate", "bin", "timeUnit", "window", etc. Ensure these objects follow the schema.
   - Other keys such as "selection", "layer", "facet", "hconcat", "vconcat", or "repeat" may be included if needed and defined in the schema.

4. **Title Property:**  
   - Include a "title" property with a string that describes the chart.

Generalized JSON Template:

{{
  "mark": "<mark_type>",         // One of: "arc", "area", "bar", "image", "line", "point", "rect", "rule", "text", "tick", "trail", "circle", "square", "geoshape"
  "encoding": {{
    "x": {{
      "field": "<x_field>",      // Must be a column from the DataFrame
      "type": "<x_type>"         // One of: "quantitative", "temporal", "ordinal", "nominal"
    }},
    "y": {{
      "field": "<y_field>",
      "type": "<y_type>"         // One of: "quantitative", "temporal", "ordinal", "nominal"
    }}
    // Additional encoding channels may be added if needed.
  }},
  "title": "<Chart Title>"
}}

Now, based on the above instructions and the provided DataFrame schema, generate a complete Vega‑Lite JSON specification. Strictly your response should be json only without any additional explanation like ```json. json response should start and end with curly braces only nothing else.
'''

prompt_template = PromptTemplate(
    input_variables=["question", "columns", "sample_data"],
    template=template
)


chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

st.title("Vega‑Lite Spec Generator with Gemini and LangChain")

st.write(
    "Enter your visualization question and generate a Vega‑Lite JSON specification based on a sample DataFrame schema.")

user_question = st.text_input("Visualization Question:", "How do the sales of each product change over time?")

if st.button("Generate Vega‑Lite Spec"):
    with st.spinner("Generating specification using Gemini..."):
        schema_info = get_dataframe_schema(df)
        # Convert schema details to JSON strings for clear formatting in the prompt.
        columns_str = json.dumps(schema_info["columns"])
        sample_data_str = json.dumps(schema_info["sample_data"])

        response = chain.run(
            question=user_question,
            columns=columns_str,
            sample_data=sample_data_str
        )

        print("===================")
        print(response)
        print("===================")

        response = response.replace("```json", "").replace("```", "")
        try:
            spec = json.loads(response)
        except Exception as e:
            st.error("Error parsing JSON from the LLM response. Please review the raw response below.")
            st.text(response)
        else:
            st.subheader("Generated Vega‑Lite JSON Specification")
            st.json(spec)
            st.subheader("Rendered Vega‑Lite Chart")
            st.vega_lite_chart(df, spec, use_container_width=True)
