import random
import psycopg2 as ps
import requests



base_url = 'https://randomuser.me/api/?nat=gb'
parties = ['NDA','INDIA','Other']
random.seed()


def generate_candidate_data(candidate_number,total_parties):
    res = requests.get(url=base_url + '&gender=' + ('female' if candidate_number%2!=0 else 'male'))
    if res.status_code == 200:
        user_data = res.json()['results'][0]
        
        return {
            'candidate_id' : user_data['login']['uuid'],
            'candidate_name': f"{user_data['name']['first']} {user_data['name']['last']}",
            'party_affiliation' : parties[candidate_number % total_parties],
            'biography' : 'Biography of a candidate',
            'campaign_platform' : 'Key campaign promises and or plateform',
            'photo_url' : user_data['picture']['large']    
        }
    else:
        return "Opps Something went wrong"





# create tables
def create_tables(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS candidate (
            candidate_id VARCHAR(255) PRIMARY KEY,
            candidate_name VARCHAR(255),
            party_affiliation VARCHAR(255),
            biography TEXT,
            campaign_platform TEXT,
            photo_url TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS voters (
            voter_id VARCHAR(255) PRIMARY KEY,
            voter_name VARCHAR(255),
            date_of_birth VARCHAR(255),
            gender VARCHAR(255),
            nationality VARCHAR(255),
            registration_number VARCHAR(255),
            address_street VARCHAR(255),
            address_city VARCHAR(255),
            address_state VARCHAR(255),
            address_country VARCHAR(255),
            address_postcode VARCHAR(255),
            email VARCHAR(255),
            phone_number VARCHAR(255),
            cell_number VARCHAR(255),
            picture TEXT,
            registered_age INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            voter_id VARCHAR(255) UNIQUE,
            candidate_id VARCHAR(255),
            voting_time TIMESTAMP,
            vote int DEFAULT 1,
            PRIMARY KEY (voter_id, candidate_id)
        )
    """)

    conn.commit()

if __name__ == "__main__":
    
    try:
        conn = ps.connect("host=host.docker.internal port=5439 dbname=voting user=postgres password=postgres")
        cur = conn.cursor( )
        
        create_tables(conn,cur)
        
        cur.execute("""
                    SELECT * FROM candidates
        """)
        
        candidates = cur.fetchall()
        print(candidates)
        
        if len(candidates) == 0:
            for i in range(3):
                candidate = generate_candidate_data(i, parties)
                print(candidate)
                cur.execute("""
                    INSERT INTO candidate(candidate_id,candidate_name,party_affiliation,biography,campaign_platform,photo_url)
                    VALUES(%s,%s,%s,%s,%s,%s) 
                    
                    """,(
                        candidate['candidate_id'],candidate['candidate_name'],candidate['party_affiliation'],candidate['biography'],candidate['campaign_platform'],candidate['photo_url']
                    ))
                conn.commit()
        
        
    except Exception as e:
        print(e)
        
    
    
    