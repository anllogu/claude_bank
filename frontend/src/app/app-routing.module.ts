import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { BalanceComponent } from './components/balance/balance.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'balance', component: BalanceComponent, canActivate: [AuthGuard] },
  { path: '', redirectTo: '/balance', pathMatch: 'full' },
  { path: '**', redirectTo: '/balance' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }