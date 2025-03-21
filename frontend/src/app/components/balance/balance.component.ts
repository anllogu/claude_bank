import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AccountService } from '../../services/account.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-balance',
  templateUrl: './balance.component.html',
  styleUrls: ['./balance.component.scss']
})
export class BalanceComponent implements OnInit {
  accountNumber: string = '';
  balance: number = 0;
  username: string = '';
  loading: boolean = true;
  error: string = '';

  constructor(
    private accountService: AccountService,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    // Obtener nombre de usuario
    const currentUser = this.authService.currentUserValue;
    if (currentUser) {
      this.username = currentUser.username;
    }
    
    this.loadBalance();
  }

  loadBalance(): void {
    this.loading = true;
    this.accountService.getBalance()
      .subscribe({
        next: (data) => {
          this.accountNumber = data.account_number;
          this.balance = data.balance;
          this.loading = false;
        },
        error: (error) => {
          this.error = error.error?.message || 'Error al cargar el saldo';
          this.loading = false;
        }
      });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}