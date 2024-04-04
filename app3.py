
import PyPDF2  # Example using PyPDF2

import os
import time

import google.generativeai as genai
import streamlit as st

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load Generative AI model
model = genai.GenerativeModel('gemini-pro')


def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def process_pdf_folder(folder_path):
  """Processes all PDF files in a folder and returns a list of summaries."""
  summaries = []
  for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
      file_path = os.path.join(folder_path, filename)
      summary = summarize_legal_pdf(file_path)
      if summary:
        summaries.append(f"**{filename} Summary:**\n{summary[:200]}...")  # Truncate for brevity
  return summaries

# Function to simulate word-by-word printing effect without new lines
def type_line_by_line(message):
    lines = message.split('\n')
    for line in lines:
        words = line.split()
        word_count = 0
        line_text = ''
        for word in words:
            if word_count < 10:
                line_text += word + ' '
                word_count += 1
            else:
                st.write(line_text)  # Print the line with 10 words
                line_text = word + ' '  # Start a new line
                word_count = 1
        st.write(line_text)  # Print the remaining words in the line
        time.sleep(0.3)


def main():
    st.title("Lawyer.AI")

    st.write("**Disclaimer:** This application's responses are for informational purposes only and do not constitute legal advice. Always consult with a licensed attorney for legal matters.")

    # Sidebar Navigation
    with st.sidebar:
        st.subheader("Navigation")
        st.text("Input")
        selected_option = st.selectbox("", ["Prompt Input", "PDF Upload"])

    # Layout for Inputs and Response
    col1, col2 = st.columns(2)

    with col1:
        if selected_option == "Prompt Input":
            st.subheader("Prompt Input")
            user_input = st.text_input("Enter your legal question:")
        elif selected_option == "PDF Upload":
            st.subheader("PDF Upload")
            uploaded_file = st.file_uploader("Upload PDF document:", type="pdf")

    with col2:
        # Generate button can be placed outside or inside col2 based on preference
        generate_text_button = st.button("Generate")

    # Stop processing if Terminate button is clicked
    if st.button("Terminate"):
        st.stop()

    # Response Container (consider styling for separation)
    response_container = st.container()
    if generate_text_button:
            if selected_option == "Prompt Input":
                if user_input:  # Moved inside conditional block
                    if is_legal_topic(user_input):
                        response = model.generate_content(user_input)
                        with response_container:
                            st.write("Response:")
                            type_line_by_line(response.text)
                    else:
                        st.write("Please ask a legal question.")
                else:
                    st.write("Please enter your legal question.")  # Handle missing input

        # PDF Processing
    if selected_option == "PDF Upload":
        if uploaded_file is not None:
            extracted_text = extract_text_from_pdf(uploaded_file)
            if extracted_text:
                if is_legal_topic(extracted_text):
                    response = model.generate_content(extracted_text)
                    with response_container:
                        st.write("Response based on uploaded PDF:")
                        type_line_by_line(response.text)
                else:
                    st.write("The uploaded PDF doesn't seem to contain legal text.")
            else:
                    st.write("Couldn't extract text from the uploaded PDF. Please try a different file.")

                
                  
def is_legal_topic(input_text):
    # Function to check if the input text contains legal keywords
    legal_keywords = ['legal',"Abscond","Bequeath",
    "Bequest",
    "Bigamy",
    "Bill of costs",
    "Bill of exchange",
    "Bill of lading",
    "Bill of sale",
    "Binding effect",
    "Binding over",
    "Binding precedent",
    "Blackmail",
    "Bodily harm",
    "Bona fide",
    "Bona vacantia",
    "Bond",
    "Bonded goods",
    "Bonded warehouse",
    "Bonus shares",
    "Book value",
    "Bought note",
    "Breach of contract",
    "Breach of duty",
    "Breach of the peace (or breaking the peace)",
    "Breach of trust",
    "Break clause",
    "Bridle way",
    "Brief",
    "Building preservation Notice",
    "Burglary",
    "Bye-law or bylaw",
    "Call",
    "Called-up capital",
    "Canon law",
    "Capacity",
    "Capital allowances",
    "Capital gain",
    "Capital gains tax",
    "Capital punishment",
    "Capital redemption reserve",
    "Careless driving",
    "Care order",
    "Cartel",
    "Case law",
    "Case stated",
    "Causation",
    "Cause of action",
    "Causing death by careless and inconsiderate driving",
    "Causing death by dangerous driving",
    "Caution",
    "Caveat",
    "Caveat emptor",
    "Central Criminal Court",
    "Certificate of Incorporation",
    "Certificate of origin",
    "Certiorari",
    "Challenge for cause",
    "Challenge to a jury",
    "Challenge to the array",
    "Challenge without Cause",
    "Chambers",
    "Chancery Division",
    "Charge",
    "Chargeable event",
    "Chargeable gain",
    "Charge certificate",
    "Charges clause",
    "Charge sheet",
    "Charges register",
    "Charging clause",
    "Charging order",
    "Charity",
    "Charity Commission",
    "Chattel",
    "Chattels personal",
    "Chattels real",
    "Cheat",
    "Cheque",
    "Cheque card",
    "Chief rent",
    "Child abuse",
    "Child assessment Order",
    "Children in care",
    "Child Support Agency",
    "Child Support Maintenance",
    "Chose",
    "Chose in action",
    "Chose in possession",
    "Circuit",
    "Circuit judge",
    "Circumstantial evidence",
    "Citation",
    "Citizen's arrest",
    "Civil court",
    "Claim",
    "Claimant",
    "Clause",
    "Clearing bank",
    "Clerk to the Justices",
    "Close company",
    "Closing order",
    "Codicil",
    "Codifying statute",
    "Coercion",
    "Collateral",
    "Commissioner for Oaths",
    "Committal for sentence",
    "Committal for trial",
    "Committal order",
    "Committal proceedings",
    "Committee of Inspection",
    "Common assault",
    "Common duty of care",
    "Common seal",
    "Commorientes",
    "Community service order",
    "Companies House",
    "Company secretary",
    "Compensation",
    "Compensation for loss of office",
    "Compensation order",
    "Completion",
    "Composition with Creditors",
    "Compulsory purchase",
    "Compulsory winding up",
    "Concealment",
    "Concealment of securities",
    "Conclusive evidence",
    "Concurrent sentence",
    "Condition",
    "Conditional agreement",
    "Conditional discharge",
    "Conditional sale agreement",
    "Condition precedent",
    "Condition subsequent",
    "Confiscation order",
    "Consecutive sentence",
    "Consent",
    "Consideration",
    "Consignee",
    "Consignor",
    "Consistory Court",
    "Conspiracy",
    "Constructive",
    "Constructive dismissal",
    "Constructive notice",
    "Consumer credit agreement",
    "Contempt of court","Contempt of court",
    "Contingency fee",
    "Contingent legacy",
    "Contract",
    "Contract for services",
    "Contract of exchange",
    "Contract of service",
    "Contributory negligence",
    "Conversion",
    "Convey",
    "Conveyance",
    "Conveyancing",
    "Conviction",
    "Copyright",
    "Coroner",
    "Corporate body (or corporation)",
    "Corporation tax",
    "Corpus",
    "Corpus delicti",
    "Counsel",
    "Counterclaim",
    "Counterfeit",
    "Counterpart",
    "County court",
    "County court judge",
    "Coupon",
    "Court of Appeal",
    "Court of Protection",
    "Covenant",
    "Creditor",
    "Creditors' voluntary winding up",
    "Criminal damage",
    "Criminal responsibility",
    "Cross-examine",
    "Crown Court",
    "Culpa",
    "Cum dividend",
    "Cumulative preference shares",
    "Curfew",
    "Customs duties",
    "Damages",
    "Dangerous driving",
    "Debenture",
    "Debt",
    "Debtor",
    "Debt securities",
    "Deceit",
    "Decree",
    "Decree absolute",
    "Decree nisi",
    "Deed",
    "Deed of arrangement",
    "De facto",
    "Defamation",
    "Default",
    "Defence",
    "Defendant",
    "De jure",
    "De minimis non curat lex",
    "Dependant",
    "Deponent",
    "Deposition",
    "Depreciation",
    "Derogation",
    "Determination",
    "Devise",
    "Devisee",
    "Diminished responsibility",
    "Diocese",
    "Diplomatic immunity",
    "Direction/directing",
    "Director",
    "Disbursement",
    "Discharge",
    "Disclaim/disclaimer",
    "Discovery",
    "Discretionary trust",
    "Disposal (dispose of)",
    "Distrain/distress",
    "Divorce",
    "Divorce petition",
    "Domicile",
    "Domiciled",
    "Domicile of choice",
    "Domicile of origin",
    "Drawee",
    "Drawer",
    "Duress",
    "Duty",
    "Easement",
    "Enabling legislation",
    "Endorsement",
    "Endowment policy",
    "Estimate",
    "Estoppel",
    "Et seq",
    "Euthanasia",
    "Excess of jurisdiction",
    "Exchange of contract",
    "Excise duty",
    "Exclusions",
    "Exclusive licence",
    "Ex dividend",
    "Execute",
    "Executed",
    "Executive director",
    "Executor",
    "Executory",
    "Executrix",
    "Exemplary damages",
    "Ex gratia",
    "Ex parte",
    "Expert witness",
    "Ex post facto",
    "Extradition",
    "Extraordinary general Meeting",
    "Extraordinary Resolution",
    "Ex works",
    "Factor",
    "False imprisonment",
    "False pretence",
    "False representation",
    "Family Division",
    "Felony",
    "Feme covert",
    "Feme sole",
    "Feu",
    "Feu duty",
    "Fiduciary",
    "Final judgement",
    "Fitness to plead",
    "Fixed charge",
    "Floating charge",
    "Forbearance",
    "Force majeure",
    "Foreclosure",
    "Forfeiture",
    "Fostering",
    "Fraud",
    "Fraudulent conveyance",
    "Fraudulent preference",
    "Fraudulent trading",
    "Freehold",
    "Free of enc",
    "Absolute",
    "Absolute discharge",
    "Abandonment",
    "Absolute owner",
    "Absolute privilege",
    "Abduction",
    "Ab initio",
    "Abovementioned",
    "Abstract of title",
    "Abuse of process",
    "Abuttals",
    "Acceptance",
    "Acceptance of service",
    "Acceptor",
    "Accessory",
    "Accomplice",
    "Accordingly",
    "Accounts",
    "Abatement:Accumulation",
    "Accused",
    "Acknowledgement",
    "Acknowledgement of Service",
    "Acquit",
    "Acquittal",
    "Action",
    "Active trust",
    "Act of bankruptcy",
    "Act of God",
    "Actual bodily harm",
    "Actual loss",
    "Actuary",
    "Actus reus",
    "Additional voluntary contribution (AVC)",
    "Ademption",
    "Ad hoc",
    "Ad idem",
    "Ad infinitum",
    "Adjourned sine die",
    "Adjournment",
    "Adjudge/adjudicate",
    "Adjudication order",
    "Administration order",
    "Administrator",
    "Admissibility of Evidence",
    "Admission",
    "Admonition",
    "Adoption",
    "Adoptive child",
    "Adoptive parent",
    "Ad valorem",
    "Adverse possession",
    "Adverse witness",
    "Advocate",
    "Affidavit",
    "Affirm",
    "Affirmation",
    "Affray",
    "Aforementioned",
    "Aforesaid",
    "Agency",
    "Agent",
    "Age of consent",
    "Aggravated assault",
    "Aggravated burglary",
    "Aggravated damages",
    "Aggravated vehicle taking",
    "Agricultural holding",
    "Aiding and abetting",
    "Airspace",
    "Alias",
    "Alibi",
    "Alien",
    "Alienation",
    "All and sundry",
    "Allegation",
    "Alleviate",
    "Allocation rate",
    "Allotment",
    "All that",
    "Alternate director",
    "Alternative verdict",
    "Amalgamation",
    "Ambiguity",
    "Ambulatory will",
    "Amnesty",
    "Ancient lights",
    "Annual accounts",
    "Annual general Meeting",
    "Annual return",
    "Annuitant",
    "Annuity",
    "Annul",
    "Ante",
    "Antecedents",
    "Antenuptial agreement",
    "Anton Piller order",
    "Appeal",
    "Appellant",
    "Appellate jurisdiction",
    "Appertaining to",
    "Applicant",
    "Appointee",
    "Appointor",
    "Appurtenances",
    "Arbitrage",
    "Arbitration",
    "Arbitrator",
    "Arraignment",
    "Arrest",
    "Arrestable offence",
    "Arson",
    "Articles",
    "Articles of association",
    "Assault",
    "Assent",
    "Asset",
    "Assign",
    "Assignment",
    "Assurance",
    "Assure",
    "Assured",
    "Assured shorthold Tenancy",
    "Attachment of earnings",
    "Attest",
    "Attorney",
    "Attorney General",
    "Audit",
    "Auditor's report",
    "Authorised share Capital",
    "Authorised Investments",
    "Autopsy",
    "Bail",
    "Bailee",
    "Bail hostel",
    "Bailiff",
    "Bailiwick",
    "Bailment",
    "Bailor",
    "Balance sheet",
    "Banker's draft",
    "Bankrupt",
    "Bankruptcy order",
    "Bankruptcy search",
    "Bar",
    "Bare trust",
    "Bare trustee",
    "Bargain and sale",
    "Barrister",
    "Barter",
    "Battery",
    "Bearer",
    "Bench",
    "Bench warrant",
    "Beneficial interest",
    "Beneficial owner",
    "Beneficiary",
 'Attorney'
,'Advocate'
,'Barrister'
,'Solicitor'
,'Counsel'
,'Jurist'
,'Lawyer'
,'Legal'
,'Litigator'
,'Paralegal'
,'Esquire'
,'Jurisprudence'
,'Litigation'
,'Counselor'
,'Legalize'
,'Defendant'
,'Plaintiff'
,'Prosecutor'
,'Defense'
,'Judge'
,'Court'
,'Law'
,'Legalize'
,'Contract'
,'Verdict'
,'Trial'
,'Brief'
,'Evidence'
,'Witness'
,'Testimony'
,'Deposition'
,'Appeal'
,'Settlement'
,'Arbitration'
,'Mediation'
,'Discovery'
,'Precedent'
,'Habeas Corpus'
,'Injunction'
,'Subpoena'
,'Pleading'
,'Complaint'
,'Indictment'
,'Affidavit'
,'Summons'
,'Cross-examination'
,'Objection'
,'Ruling'
,'Statute'
,'Constitution'
,'Legalize'
,'Contract'
,'Verdict'
,'Trial'
,'Brief'
,'Evidence'
,'Witness'
,'Testimony'
,'Deposition'
,'Appeal'
,'Settlement'
,'Arbitration'
,'Mediation'
,'Discovery'
,'Precedent'
,'Habeas Corpus'
,'Injunction'
,'Subpoena'
,'Pleading'
,'Complaint'
,'Indictment'
,'Affidavit'
,'Summons'
,'Cross-examination'
,'Objection'
,'Ruling'
,'Statute'
,'Constitution'
,'Legalize'
,'Contract'
,'Verdict'
,'Trial'
,'Brief'
,'Evidence'
,'Witness'
,'Testimony'
,'Deposition'
,'Appeal'
,'Settlement'
,'Arbitration'
,'Mediation'
,'Discovery'
,'Precedent'
,'Habeas Corpus'
,'Injunction'
,'Subpoena'
,'Pleading'
,'Complaint'
,'Indictment'
,'Affidavit']  # List of legal keywords
    for keyword in legal_keywords:
        if keyword.lower() in input_text.lower():
            return True
    return False

if __name__ == "__main__":
    main()
