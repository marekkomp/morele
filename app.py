import streamlit as st
import pandas as pd
import os
from datetime import datetime

def transform_to_morele_schema(input_df):
    # Define the Morele schema
    morele_columns = [
        "vendorPartNumber", "salePriceBrutto", "currency", "vendorProductName",
        "barcodes", "availability", "quantity", "vendorBrandName",
        "brandCode", "vat", "images", "vendorDescription",
        "warranty", "vendorCharacteristic", "vendorCategoryName",
        "deliveryDays", "deliveryPrice", "productPromotionActive",
        "productPromotionCampaignName", "productPromotionPrice"
    ]

    # Create a DataFrame with the required columns
    output_df = pd.DataFrame(columns=morele_columns)

    # Match and copy data from the input DataFrame if columns exist
    for col in morele_columns:
        if col in input_df.columns:
            output_df[col] = input_df[col]

    # Fill missing required columns with default values
    output_df["vendorPartNumber"] = output_df["vendorPartNumber"].fillna("MISSING_SKU")
    output_df["currency"] = output_df["currency"].fillna("PLN")
    output_df["availability"] = output_df["availability"].fillna(0)

    return output_df

# Streamlit app
def main():
    st.title("CSV Transformer for Morele Schema")

    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

    if uploaded_file is not None:
        # Read the uploaded CSV file
        input_df = pd.read_csv(uploaded_file)
        st.write("### Uploaded File Data")
        st.dataframe(input_df)

        # Transform data to match Morele schema
        transformed_df = transform_to_morele_schema(input_df)

        st.write("### Transformed Data")
        st.dataframe(transformed_df)

        # Save the transformed data as a new CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"morele_transformed_{timestamp}.csv"
        transformed_df.to_csv(output_filename, index=False)

        st.success(f"File transformed and saved as {output_filename}")

        # Add a download button
        with open(output_filename, "rb") as file:
            btn = st.download_button(
                label="Download Transformed File",
                data=file,
                file_name=output_filename,
                mime="text/csv"
            )

        # GitHub integration
        github_repo = "marekkomp/morele"
        github_command = f"git add {output_filename} && git commit -m \"Add transformed CSV {output_filename}\" && git push"

        st.write("### Save to GitHub")
        st.code(github_command, language="bash")
        st.info("Run the above command in your terminal to save the file to your GitHub repository.")

if __name__ == "__main__":
    main()
