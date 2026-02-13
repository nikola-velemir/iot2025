import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {Navbar} from './navbar/navbar';
import {LoaderDirective} from './services/loader/loading-directive';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Navbar, LoaderDirective],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('Smart home');
}
