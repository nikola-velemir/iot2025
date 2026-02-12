import { Component } from '@angular/core';
import {RouterLink, RouterLinkActive} from '@angular/router';
import {NgStyle} from '@angular/common';

interface NavItem {
  label: string;
  icon: string;
  link: string;
  color: string;
}

@Component({
  selector: 'app-navbar',
  imports: [
    RouterLink,
    RouterLinkActive,
    NgStyle
  ],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss',
})
export class Navbar {
  alarmState: boolean = false;

  topbarItems: NavItem[] = [
    {label: 'Raspberry Pi 1', icon: 'home_iot_device', link: '/pi1', color: '#FFBF58'},
    {label: 'Raspberry Pi 2', icon: 'home_iot_device', link: '/pi2', color: '#58FF68'},
    {label: 'Raspberry Pi 3', icon: 'home_iot_device', link: '/pi3', color: '#A0D1FF'},
  ];
}
