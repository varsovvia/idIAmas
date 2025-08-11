#!/usr/bin/env python3
"""
Test script specifically for the fade overlay functionality.
Creates a popup with many grammar cards to demonstrate scrolling and fade effect.
"""

import sys
from PyQt6.QtWidgets import QApplication
from popup_refactored import PopupWindow

def create_extensive_test_data():
    """Create test data with many grammar items to test scrolling and fade"""
    return {
        'original': 'Ciao, come stai? Sto bene, grazie. E tu? Anch\'io sto bene. Che cosa fai oggi? Vado al lavoro.',
        'translation': 'Hola, ¿cómo estás? Estoy bien, gracias. ¿Y tú? Yo también estoy bien. ¿Qué haces hoy? Voy al trabajo.',
        'grammar': '''- Ciao: hola (saludo informal italiano)
- come: cómo (adverbio interrogativo)
- stai: estás (segunda persona del verbo 'stare' - estar/quedarse)
- Sto: estoy (primera persona del verbo 'stare')
- bene: bien (adverbio de modo)
- grazie: gracias (expresión de cortesía)
- E: y (conjunción copulativa)
- tu: tú (pronombre personal de segunda persona)
- Anch'io: yo también (contracción de 'anche io')
- anche: también (adverbio)
- io: yo (pronombre personal de primera persona)
- Che: qué (pronombre interrogativo)
- cosa: cosa (sustantivo femenino)
- fai: haces (segunda persona del verbo 'fare' - hacer)
- oggi: hoy (adverbio de tiempo)
- Vado: voy (primera persona del verbo 'andare' - ir)
- al: al (contracción de 'a' + 'il')
- a: a (preposición de dirección)
- il: el (artículo determinado masculino singular)
- lavoro: trabajo (sustantivo masculino)
- molto: mucho (adverbio de cantidad)
- bello: bello/hermoso (adjetivo calificativo masculino)
- grande: grande (adjetivo calificativo invariable)
- piccolo: pequeño (adjetivo calificativo masculino)
- rosso: rojo (adjetivo de color masculino)
- blu: azul (adjetivo de color invariable)
- verde: verde (adjetivo de color invariable)
- giallo: amarillo (adjetivo de color masculino)
- nero: negro (adjetivo de color masculino)
- bianco: blanco (adjetivo de color masculino)
- casa: casa (sustantivo femenino)
- strada: calle (sustantivo femenino)
- macchina: coche (sustantivo femenino)
- treno: tren (sustantivo masculino)
- aereo: avión (sustantivo masculino)
- mare: mar (sustantivo masculino)
- montagna: montaña (sustantivo femenino)
- città: ciudad (sustantivo femenino invariable)
- paese: pueblo/país (sustantivo masculino)
- mondo: mundo (sustantivo masculino)
- tempo: tiempo (sustantivo masculino)
- anno: año (sustantivo masculino)
- mese: mes (sustantivo masculino)
- settimana: semana (sustantivo femenino)
- giorno: día (sustantivo masculino)
- ora: hora (sustantivo femenino)
- minuto: minuto (sustantivo masculino)
- secondo: segundo (sustantivo masculino)
- famiglia: familia (sustantivo femenino)
- amico: amigo (sustantivo masculino)
- persona: persona (sustantivo femenino)
- uomo: hombre (sustantivo masculino)
- donna: mujer (sustantivo femenino)
- bambino: niño (sustantivo masculino)
- bambina: niña (sustantivo femenino)
- ragazzo: chico (sustantivo masculino)
- ragazza: chica (sustantivo femenino)
- cibo: comida (sustantivo masculino)
- acqua: agua (sustantivo femenino)
- vino: vino (sustantivo masculino)
- caffè: café (sustantivo masculino invariable)
- latte: leche (sustantivo masculino)
- pane: pan (sustantivo masculino)
- formaggio: queso (sustantivo masculino)
- carne: carne (sustantivo femenino)
- pesce: pescado (sustantivo masculino)
- frutta: fruta (sustantivo femenino)
- verdura: verdura (sustantivo femenino)'''
    }

def main():
    """Test the fade overlay with extensive content"""
    # Qt6 handles high DPI support automatically
    app = QApplication(sys.argv)
    
    # Create popup with extensive test data
    test_data = create_extensive_test_data()
    popup = PopupWindow(test_data)
    popup.show()
    
    print("🎯 Fade Overlay Test Running!")
    print("📋 Test Instructions:")
    print("   1. Switch to the '※ Grammar' tab")
    print("   2. Scroll down to see the fade effect")
    print("   3. Notice how cards blend smoothly into background")
    print("   4. Test resize behavior by changing window size")
    print("   5. Press Esc to close popup")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
