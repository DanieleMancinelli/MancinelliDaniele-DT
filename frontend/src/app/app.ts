import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DeliveryService } from './services/delivery';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent implements OnInit {
  deliveries: any[] = [];
  
  // Modello per la nuova consegna
  newDelivery = {
    tracking_code: '',
    recipient: '',
    address: '',
    time_slot: '',
    priority: 'MEDIUM' // Valore di default
  };

  constructor(
    private deliveryService: DeliveryService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadDeliveries();
  }

  loadDeliveries() {
    this.deliveryService.getDeliveries().subscribe({
      next: (data) => {
        this.deliveries = data;
        this.cdr.detectChanges();
      },
      error: (err) => console.error(err)
    });
  }

  submitDelivery() {
    // Validazione base
    if (!this.newDelivery.tracking_code.trim() || !this.newDelivery.recipient.trim()) {
      alert("Tracking e Destinatario sono obbligatori!");
      return;
    }

    this.deliveryService.addDelivery(this.newDelivery).subscribe({
      next: () => {
        // Reset del form
        this.newDelivery = {
          tracking_code: '',
          recipient: '',
          address: '',
          time_slot: '',
          priority: 'MEDIUM'
        };
        this.loadDeliveries(); // Aggiorna la lista
      },
      error: (err) => {
        alert(err.error.error || "Errore durante il salvataggio");
      }
    });
  }

  changeStatus(id: number, newStatus: string) {
    this.deliveryService.updateStatus(id, newStatus).subscribe({
      next: () => {
        this.loadDeliveries(); // Ricarica la lista per aggiornare i colori dei bordi
      },
      error: (err) => alert("Errore nel cambio stato")
    });
  }
}