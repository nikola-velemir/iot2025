import {Directive, ElementRef, HostListener, Input, OnDestroy, OnInit} from '@angular/core';
import {NgModel} from '@angular/forms';
import {Subscription} from 'rxjs';

@Directive({
  selector: '[appCappedNumber]',
})
export class CappedNumber implements OnInit, OnDestroy {
  @Input() capMin = 1;
  @Input() capMax = Number.MAX_SAFE_INTEGER;
  @Input() canBeEmpty = false;

  private modelSubscription?: Subscription;

  constructor(
    private el: ElementRef<HTMLInputElement>,
    private ngModel: NgModel,
  ) {}

  ngOnInit() {
    this.modelSubscription = this.ngModel.valueChanges?.subscribe((value) => {
      const numericValue = typeof value === 'string' ? Number(value.replace(/\D/g, '')) : value;

      if (value && value !== value.toLocaleString('en-US')) {
        this.writeCapped(numericValue);
      }
    });
  }

  ngOnDestroy() {
    this.modelSubscription?.unsubscribe();
  }

  getCurrentValue() {
    return Number(this.el.nativeElement.value);
  }

  @HostListener('keydown', ['$event'])
  onKeyDown(event: KeyboardEvent) {
    const allowed = [
      'Backspace',
      'Delete',
      'ArrowLeft',
      'ArrowRight',
      'Tab',
    ];

    if (event.ctrlKey || event.metaKey || allowed.includes(event.key)) return;

    if (!/^\d$/.test(event.key)) {
      event.preventDefault();
      return;
    }

    let current = this.getCurrentValue();
    if (Number.isFinite(current) && current >= this.capMax) {
      event.preventDefault();
    }
  }

  @HostListener('paste', ['$event'])
  onPaste(event: ClipboardEvent) {
    event.preventDefault();

    const pasted = event.clipboardData?.getData('text') ?? '';
    const digits = pasted.replace(/\D/g, '');

    const num = digits ? Number(digits) : this.capMin;
    this.writeCapped(num);
  }

  @HostListener('input')
  onInput() {
    const value = this.el.nativeElement.value;
    const digits = value.replace(/\D/g, '');

    if (digits === '' && !this.canBeEmpty) {
      this.writeCapped(this.capMin);
      return;
    } else if (digits === '' && this.canBeEmpty) {
      this.writeEmpty();
      return;
    }

    this.writeCapped(Number(digits));
  }

  writeCapped(value: number) {
    let num = Number(value);

    if (!Number.isFinite(num)) {
      num = this.capMin;
    }

    num = Math.floor(num);

    if (num < this.capMin) num = this.capMin;
    if (num > this.capMax) num = this.capMax;

    this.writeString(num);
    this.ngModel.viewToModelUpdate(num);
  }

  writeString(value: number) {
    this.el.nativeElement.value = value.toLocaleString('en-US');
  }

  writeEmpty() {
    this.el.nativeElement.value = '';
  }
}
