import {Injectable, Renderer2, RendererFactory2, signal} from '@angular/core';

@Injectable({ providedIn: 'root' })
export class LoadingService {
  private _loading = signal(false);
  readonly isLoading = this._loading.asReadonly();
  private keyListenerFn?: () => void;
  private renderer: Renderer2;

  private activeRequests = 0;

  constructor(rendererFactory: RendererFactory2) {
    this.renderer = rendererFactory.createRenderer(null, null);
  }

  show() {
    if (this.activeRequests === 0) {
      this._loading.set(true);
      this.blockKeyboard();
    }
    this.activeRequests++;
  }

  hide() {
    this.activeRequests--;
    if (this.activeRequests <= 0) {
      this.activeRequests = 0;
      this.unblockKeyboard();
      this._loading.set(false);
    }
  }

  private blockKeyboard() {
    this.keyListenerFn = this.renderer.listen('window', 'keydown', (event: KeyboardEvent) => {
      if (this._loading()) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
      }
    });
  }

  private unblockKeyboard() {
    if (this.keyListenerFn) {
      this.keyListenerFn();
      this.keyListenerFn = undefined;
    }
  }
}
