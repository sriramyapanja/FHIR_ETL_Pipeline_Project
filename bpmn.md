# BPMN Model Page

[Home](./index.md) ||
[BPMN Model](./bpmn.md) ||
[Use Case Model](./use_case.md) ||
[ETL Pipeline](./etl_pipeline.md) ||
[Insights](./insights.md) ||
[Team Contributions](./team_contrib.md) ||
[About](./about.md) ||

![bpmn_sample](./assets/Bpmn_model.png)

 Patient Referral from Primary Care to Hospital 

The process begins at the Primary Care Clinic, where a referral is initiated for a patient requiring specialist treatment. The clinic updates the patient’s referral details, including the reason for the referral and any supporting documentation, and communicates this information to the hospital. 

 Referral Review and Patient Registration at the Hospital 

Upon receiving the referral, the hospital reviews the details to ensure accuracy and appropriateness. The patient is registered in the hospital system, and their information is entered into the Electronic Health Record (EHR) to facilitate the care process. 

 Specialist Evaluation and Treatment 

A specialist evaluates the patient’s condition to determine the appropriate course of treatment. The specialist provides the necessary care. A decision gateway is used where the specialist evaluates whether further treatment is necessary in other departments.

 Decision on Further Treatment 

If patient  needs further treatments, they are referred to primary care or else  discharged from the hospital. Meanwhile both the discharged patient’s and the referred patients’s treatment details are conveyed to primary care and documented in hospital EHR.

 
Post-treatment, the hospital documents a comprehensive treatment summary, including outcomes and recommendations. This summary is shared with the Primary Care Clinic to ensure continuity of care. 

 Follow-Up Care Coordination at Primary Care 

The Primary Care Clinic updates the patient’s medical records with the information provided by the hospital. If needed, follow-up appointments are scheduled to address any ongoing patient needs, completing the care coordination process. 

 