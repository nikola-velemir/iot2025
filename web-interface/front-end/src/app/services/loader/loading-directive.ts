import { Directive, ElementRef, Renderer2, ComponentRef, ViewContainerRef, effect, inject } from '@angular/core';
import {LoadingService} from './loading.service';
import {LoadingOverlayComponent} from './loading-overlay';

@Directive({
  selector: '[appLoader]',
  standalone: true
})
export class LoaderDirective {
  private loadingService = inject(LoadingService);
  private el = inject(ElementRef);
  private renderer = inject(Renderer2);
  private viewContainer = inject(ViewContainerRef);

  private spinnerRef?: ComponentRef<LoadingOverlayComponent>;

  constructor() {
    this.renderer.setStyle(this.el.nativeElement, 'position', 'relative');

    effect(() => {
      const isGlobalLoading = this.loadingService.isLoading();
      isGlobalLoading ? this.show() : this.hide();
    });
  }

  private show() {
    if (!this.spinnerRef) {
      this.spinnerRef = this.viewContainer.createComponent(LoadingOverlayComponent);
      const loader = this.spinnerRef.location.nativeElement;

      this.renderer.setStyle(loader, 'position', 'absolute');
      this.renderer.setStyle(loader, 'top', '0');
      this.renderer.setStyle(loader, 'left', '0');
      this.renderer.setStyle(loader, 'width', '100%');
      this.renderer.setStyle(loader, 'height', '100%');
      this.renderer.setStyle(loader, 'display', 'flex');
      this.renderer.setStyle(loader, 'justify-content', 'center');
      this.renderer.setStyle(loader, 'align-items', 'center');
      this.renderer.setStyle(loader, 'background', 'rgba(0, 0, 0, 0.15)');
      this.renderer.setStyle(loader, 'z-index', '99999');
      this.renderer.setStyle(loader, 'pointer-events', 'all');
      this.renderer.setStyle(loader, 'cursor', 'wait');

      this.renderer.appendChild(this.el.nativeElement, loader);
    }
  }

  private hide() {
    if (this.spinnerRef) {
      this.spinnerRef.destroy();
      this.spinnerRef = undefined;
    }
  }
}
