def get_companies() -> list[str]:
    try:
        from .api import org_db
        domains = []
        for key in org_db["domain"].keys():
            domains.append(org_db["domain"][key])
        
        return domains
    except Exception as e:
        return [f"Error retrieving companies: {e}"]


def update_org_info(domain: str, data: dict):
    try:
        from .api import org_db
        id = list(org_db["domain"].keys())[list(org_db["domain"].values()).index(domain)]

        # If the domain index was found, proceed with updating values
        if id is not None:
            for key in org_db.keys():
                try:
                    if key == "industry":
                        try:
                            org_db[key][str(id)] = data["organization"]["industries"][0]
                        except Exception as e:
                            org_db[key][str(id)] = f"[ERROR @ key == industry] {e}"
                    else:
                        org_db[key][str(id)] = data["organization"][key]
                except Exception:
                    continue
                
            print(f"Updated data for {domain} successfully!")

        else:
            print(f"Domain {domain} not found!")
            raise Exception("Domain not found!")

    except Exception as e:
        print(f"[ERROR @ excel_manager/update_info()] {e}")