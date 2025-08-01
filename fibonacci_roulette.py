"""
Auteur : VERGEYLEN Anthony
Date   : 01/08/2025
Projet : Simulateur de roulette utilisant la stratégie Fibonacci
Description :
Ce programme simule le jeu de la roulette en suivant la méthode Fibonacci pour les mises.
Il propose plusieurs modes : debug, simulation multiple, mode manuel, et une explication pédagogique.
"""

import random
import time


class FibonacciRoulette:
    def __init__(self, start_balance: int = 1000, max_bet: int = 500):
        """
        Initialise le simulateur avec un solde initial et une mise maximale.
        :param start_balance: Solde de départ du joueur
        :param max_bet: Mise maximale autorisée
        """
        self.initial_balance = start_balance
        self.max_bet = max_bet
        self.fibonacci = self._generate_fibonacci_sequence(max_bet)

    def _generate_fibonacci_sequence(self, limit: int) -> list:
        """
        Génère une suite de Fibonacci jusqu'à une limite donnée.
        :param limit: Valeur maximale de la suite
        :return: Liste des valeurs Fibonacci
        """
        seq = [1, 1]
        while seq[-1] + seq[-2] <= limit:
            seq.append(seq[-1] + seq[-2])
        return seq

    def _simulate_once(self, total_rounds=50, bet_on=0, base_bet=1, verbose=False):
        """
        Simule une session de jeu en suivant la stratégie Fibonacci.
        :param total_rounds: Nombre de tours à simuler
        :param bet_on: 0 pour noir ⚫️, 1 pour rouge 🔴
        :param base_bet: Mise de départ
        :param verbose: Affiche les détails de chaque tour
        :return: Solde final après la session
        """
        balance = self.initial_balance
        fib = [base_bet, base_bet]
        while fib[-1] + fib[-2] <= self.max_bet:
            fib.append(fib[-1] + fib[-2])

        fib_index = 0
        current_bet = fib[fib_index]

        for round_num in range(1, total_rounds + 1):
            if balance <= 0:
                if verbose:
                    print(f"\n💸 Solde épuisé à la fin du tour {round_num - 1}. Vous ne pouvez plus miser.")
                break

            if current_bet > balance:
                if verbose:
                    print(f"\n❌ Solde insuffisant pour miser {current_bet}€ (solde : {balance}€). Fin de la partie.")
                break

            result = random.choice([0, 1])  # 0 = noir ⚫️, 1 = rouge 🔴
            win = result == bet_on
            boule = "⚫️" if result == 0 else "🔴"

            if win:
                balance += current_bet
                fib_index = max(0, fib_index - 2)
            else:
                balance -= current_bet
                fib_index = min(len(fib) - 1, fib_index + 1)

            current_bet = min(fib[fib_index], self.max_bet)

            if verbose:
                print(
                    f"Tour {round_num:02d} | Résultat : {boule} | Mise : {current_bet}€ | "
                    f"{'GAGNÉ ✅' if win else 'PERDU ❌'} | Solde : {balance}€"
                )
                time.sleep(0.03)

        return balance

    def _simulate_multiple(self, times, total_rounds=50, bet_on=0, base_bet=1):
        """
        Simule plusieurs sessions de jeu pour estimer la rentabilité de la stratégie.
        :param times: Nombre de simulations
        :param total_rounds: Nombre de tours par simulation
        :param bet_on: Couleur misée (0 = noir, 1 = rouge)
        :param base_bet: Mise de départ
        :return: Dictionnaire des statistiques
        """
        total_start = self.initial_balance * times
        total_final = 0
        gains = 0

        for _ in range(times):
            result = self._simulate_once(total_rounds=total_rounds, bet_on=bet_on, base_bet=base_bet)
            total_final += result
            if result > self.initial_balance:
                gains += 1

        return {
            "simulations": times,
            "win_rate": (gains / times) * 100,
            "avg_balance": total_final / times,
            "total_gain": total_final - total_start,
            "total_start": total_start,
            "total_final": total_final
        }

    def display_stat_summary(self, stats):
        """Affiche un résumé lisible des statistiques d’une simulation multiple."""
        print(
            f"\n📊 {stats['simulations']} simulations : "
            f"taux de gain {stats['win_rate']:.2f}% | "
            f"solde moyen : {stats['avg_balance']:.2f}€ | "
            f"gain total estimé : {stats['total_gain']:.2f}€"
        )
        print(
            f"     ➤ Total misé : {stats['total_start']:.2f}€ | "
            f"Total récupéré : {stats['total_final']:.2f}€ | "
            f"Bilan : {'✅ +' if stats['total_gain'] >= 0 else '❌ '}{abs(stats['total_gain']):.2f}€"
        )

    def ask_user_to_play(self):
        """Mode interactif où l’utilisateur entre sa couleur, mise et nombre de tours."""
        print("\n🎰 Mode 'Jouer à la roulette' (technique Fibonacci)")
        try:
            mise = int(input("💵 Combien souhaitez-vous miser au premier tour ? (min. 1) : ").strip())
            couleur = input("🎨 Sur quelle couleur souhaitez-vous miser ? (noir/rouge) : ").strip().lower()
            tours = int(input("🔁 Combien de tours souhaitez-vous jouer ? : ").strip())
        except Exception:
            print("❌ Entrée invalide. Abandon.")
            return

        if couleur not in ["noir", "rouge"]:
            print("❌ Couleur invalide. Utilisez 'noir' ou 'rouge'.")
            return

        if mise > self.initial_balance // 2:
            print("⚠️ Mise trop élevée par rapport à votre capital. Veuillez réessayer avec un montant plus raisonnable.")
            return

        bet_on = 0 if couleur == "noir" else 1

        print(f"\n🎯 Vous allez miser sur {'⚫️ NOIR' if bet_on == 0 else '🔴 ROUGE'} pendant {tours} tours.")
        result = self._simulate_once(total_rounds=tours, bet_on=bet_on, base_bet=mise, verbose=True)

        print("\n📌 Résultat final :")
        print(f" - Solde de départ : {self.initial_balance}€")
        print(f" - Solde final : {result}€")
        print(f" - {'GAIN ✅' if result > self.initial_balance else 'PERTE ❌'} de {abs(result - self.initial_balance)}€")

    def explain_fibonacci_strategy(self):
        """Affiche une explication claire de la stratégie Fibonacci appliquée à la roulette."""
        print("\n🎓 Stratégie Fibonacci à la roulette :\n")
        print("Tu vas jouer uniquement sur des chances simples (rouge/noir, pair/impair, manque/passe),")
        print("qui ont environ 48,6% de chance de gagner en roulette européenne (car il y a un seul 0).\n")
        print("📐 Le principe de la méthode Fibonacci :")
        print("1. Tu commences avec une mise de base (ex : 1€).")
        print("2. Si tu perds, tu avances dans la suite : 1 → 1 → 2 → 3 → 5 → 8 → 13 → ...")
        print("3. Si tu gagnes, tu recules de deux positions dans la suite.")
        print("4. Le but est de récupérer les pertes progressivement.\n")
        print("✅ Moins agressif que la martingale\n❌ Mais requiert un bon capital en cas de pertes longues\n")
        print("👉 Relance le programme pour tester toi-même !")

    def run(self):
        """Point d'entrée principal du programme : affiche les choix et exécute la logique correspondante."""
        print("🎰 Bienvenue dans le simulateur de roulette (stratégie Fibonacci)\n")
        print("📌 Règles du jeu :")
        print(" - C’est une roulette européenne 🎡 (1 seul zéro)")
        print(" - Tu peux miser sur des chances simples : rouge 🔴 / noir ⚫️")
        print(" - Mise de départ par défaut : 1€ (modifiable)")
        print(" - La mise maximale est limitée à 500€\n")

        print("Choisissez un mode :")
        print(" 1 - Mode Automatique DEBUG (détail des 50 premiers tours)")
        print(" 2 - Mode Automatique SIMPLE (résumé uniquement)")
        print(" 3 - Jouer à la roulette manuellement 🎮")
        print(" 4 - Comprendre la stratégie Fibonacci 🎓")

        choix = input("Entrez 1, 2, 3 ou 4 : ").strip()

        if choix == "1":
            print("\n🔧 Lancement en mode DEBUG...\n")
            final = self._simulate_once(verbose=True)
            print(f"\n📌 Résultat DEBUG — solde final : {final}€ (gain de {final - self.initial_balance}€)")

        elif choix == "2":
            print("\n📊 Mode Automatique Simple :")
            for count in [100, 200, 500, 1000, 5000, 50000]:
                stats = self._simulate_multiple(times=count)
                self.display_stat_summary(stats)

        elif choix == "3":
            self.ask_user_to_play()

        elif choix == "4":
            self.explain_fibonacci_strategy()

        else:
            print("❌ Choix invalide. Fermeture.")


if __name__ == "__main__":
    simulator = FibonacciRoulette(start_balance=1000, max_bet=500)
    simulator.run()
