import { useCallback, useEffect, useRef, useState } from "react";
import EventEmitter from "events";
import TypedEmitter from "typed-emitter";
import { useObject } from "./use-object";

export const useDragHelper = ({ button = 0 }: { button?: number } = {}) => {
  const [dragState, setDragState] = useState<DragState>({
    isDragging: false,
  });

  const emitter = useRef(new EventEmitter() as DragEventsEmitter);

  useEffect(() => {
    if (!dragState.isDragging) return;

    const mousemove = (e: MouseEvent) => {
      if (e.buttons & (1 << button)) {
        const coords = mouseCoordinates(e);

        emitter.current.emit("drag", {
          ...coords,
          start: dragState.start!,
          originalEvent: e,
        });
      } else {
        const coords = mouseCoordinates(e);

        emitter.current.emit("dragend", {
          ...coords,
          start: dragState.start!,
          drop: null,
          originalEvent: e,
        });

        setDragState((state) => ({
          ...state,
          isDragging: false,
          drop: null,
        }));
      }
    };

    const mouseup = (e: MouseEvent) => {
      if (e.button === button) {
        const coords = mouseCoordinates(e);

        emitter.current.emit("dragend", {
          ...coords,
          start: dragState.start!,
          drop: coords,
          originalEvent: e,
        });

        setDragState((state) => ({
          ...state,
          isDragging: false,
          drop: coords,
        }));
      }
    };

    window.addEventListener("mousemove", mousemove);
    window.addEventListener("mouseup", mouseup);

    return () => {
      window.removeEventListener("mousemove", mousemove);
      window.removeEventListener("mouseup", mouseup);
    };
  }, [dragState.isDragging]);

  return useObject({
    props: useObject({
      onMouseDown: useCallback((e: React.MouseEvent) => {
        if (e.button === button) {
          e.preventDefault();

          const coords = mouseCoordinates(e.nativeEvent);

          emitter.current.emit("dragstart", {
            ...coords,
            originalEvent: e.nativeEvent,
          });

          setDragState((state) => ({
            ...state,
            isDragging: true,
            start: coords,
          }));
        }
      }, []),
    }),

    events: emitter.current as Omit<DragEventsEmitter, "emit">,

    state: useObject(dragState),

    useEventListener: <E extends keyof DragEvents>(
      event: E,
      listener: DragEvents[E],
      deps: any[]
    ) => {
      useEffect(() => {
        emitter.current.on(event, listener);
        return () => {
          emitter.current.off(event, listener);
        };
      }, deps);
    },
  });
};

type MouseCoordinates = {
  clientX: number;
  clientY: number;
  screenX: number;
  screenY: number;
  pageX: number;
  pageY: number;
  offsetX: number;
  offsetY: number;
};

const mouseCoordinates = (e: MouseEvent) => ({
  clientX: e.clientX,
  clientY: e.clientY,
  screenX: e.screenX,
  screenY: e.screenY,
  pageX: e.pageX,
  pageY: e.pageY,
  offsetX: e.offsetX,
  offsetY: e.offsetY,
});

interface DragState {
  isDragging: boolean;
  start?: MouseCoordinates;
  drop?: MouseCoordinates | null;
}

export interface DragStartEvent extends MouseCoordinates {
  originalEvent: MouseEvent;
}

export interface DragEvent extends MouseCoordinates {
  start: MouseCoordinates;
  originalEvent: MouseEvent;
}

export interface DragEndEvent extends MouseCoordinates {
  start: MouseCoordinates;
  drop: MouseCoordinates | null;
  originalEvent: MouseEvent;
}

type DragEvents = {
  dragstart(e: DragStartEvent): void;
  drag(e: DragEvent): void;
  dragend(e: DragEndEvent): void;
};

type DragEventsEmitter = TypedEmitter<DragEvents>;
