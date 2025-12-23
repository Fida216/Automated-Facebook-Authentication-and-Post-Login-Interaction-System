import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def automate_facebook_post(email, password, content):
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("Ouverture de Facebook...")
        driver.get("https://www.facebook.com")
        time.sleep(5)
        
        print("Connexion automatique...")
        email_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.clear()
        email_field.send_keys(email)
        
        pass_field = driver.find_element(By.NAME, "pass")
        pass_field.clear()
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.RETURN)
        
        print("Connexion en cours... Résolvez le reCAPTCHA manuellement si nécessaire.")
        time.sleep(10)
        
        # Attente page d'accueil (élément stable)
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//div[@role='main']")))
        print("Connecté avec succès !")
        
        # Bouton création post (robust pour design 2025)
        post_button_xpath = (
            "//div[@role='button' and (contains(@aria-label, 'Créer une publication') or contains(@aria-label, 'quoi pensez-vous'))] | "
            "//span[contains(text(), 'quoi pensez-vous')]/ancestor::div[@role='button'] | "
            "//div[contains(@aria-label, 'Créer une publication') or contains(@aria-label, 'quoi pensez-vous')]"
        )
        
        post_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, post_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_button)
        time.sleep(1)
        post_button.click()
        print("Modale ouverte.")
        time.sleep(3)
        
        # Zone de texte (focus + saisie)
        post_box = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox' and @contenteditable='true']")))
        post_box.click()
        post_box.clear()
        post_box.send_keys(content)
        print("Texte saisi : " + content)
        time.sleep(2)
        
        # Bouton Publier (activé seulement après texte)
        publish_button_xpath = "//div[@role='button' and contains(@aria-label, 'Publier') and not(contains(@aria-disabled, 'true'))]"
        
        publish_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, publish_button_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", publish_button)
        time.sleep(1)
        publish_button.click()
        
        time.sleep(8)
        print("Publication réussie ! Le post est maintenant sur votre profil.")
    
    except TimeoutException as te:
        print("Timeout : Élément non trouvé (changement Facebook probable).")
        driver.save_screenshot("timeout_erreur.png")
    except Exception as e:
        print(f"Erreur : {e}")
        driver.save_screenshot("erreur_facebook.png")
        print("Capture d'écran sauvegardée → ouvrez-la pour voir où ça bloque (modale ouverte ? texte saisi ?)")
    
    finally:
        input("Appuyez sur Entrée pour fermer le navigateur...")
        driver.quit()

if __name__ == "__main__":
    print("=== Automatisation Facebook - Publication fonctionnelle décembre 2025 ===")
    user_email = input("Entrez votre email ou téléphone Facebook : ")
    user_pass = input("Entrez votre mot de passe : ")
    post_content = input("Entrez le texte à publier : ")
    
    automate_facebook_post(user_email, user_pass, post_content)
