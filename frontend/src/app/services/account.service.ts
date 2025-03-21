import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

interface AccountBalance {
  account_number: string;
  balance: number;
}

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  
  constructor(private http: HttpClient) { }
  
  getBalance(): Observable<AccountBalance> {
    return this.http.get<AccountBalance>(`${environment.apiUrl}/balance`);
  }
}