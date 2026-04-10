// Configuración de la URL del backend
// En desarrollo usa localhost, en producción usa variable de entorno
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const RETRYABLE_STATUS = new Set([502, 503, 504, 522, 524]);

function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchWithRetry(url, options = {}, config = {}) {
	const {
		retries = 2,
		retryDelayMs = 600,
		timeoutMs = 20000
	} = config;

	const method = (options.method || 'GET').toUpperCase();
	const shouldRetry = method === 'GET';

	let lastError = null;

	for (let attempt = 0; attempt <= retries; attempt++) {
		const controller = new AbortController();
		const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

		try {
			const response = await fetch(url, {
				...options,
				signal: controller.signal
			});

			clearTimeout(timeoutId);

			const canRetryStatus = shouldRetry && RETRYABLE_STATUS.has(response.status);
			const hasMoreAttempts = attempt < retries;

			if (canRetryStatus && hasMoreAttempts) {
				await sleep(retryDelayMs * (attempt + 1));
				continue;
			}

			return response;
		} catch (error) {
			clearTimeout(timeoutId);
			lastError = error;

			if (!shouldRetry || attempt >= retries) {
				throw error;
			}

			await sleep(retryDelayMs * (attempt + 1));
		}
	}

	throw lastError || new Error('Error de red');
}

async function getJson(path, fallbackMessage) {
	try {
		const response = await fetchWithRetry(`${API_BASE}${path}`);
		if (!response.ok) {
			throw new Error(await getErrorMessage(response, fallbackMessage));
		}
		return response.json();
	} catch {
		throw new Error(`${fallbackMessage} (intenta nuevamente en unos segundos)`);
	}
}

async function getErrorMessage(response, fallback) {
	let message = fallback;
	try {
		const data = await response.json();
		if (data?.detail) message = data.detail;
	} catch {
		// no-op
	}
	return message;
}

export async function fetchJugadores() {
	return getJson('/Jugadores/', 'Error al cargar jugadores');
}

export async function cargarJugador(jugadorData) {
	const response = await fetch(`${API_BASE}/Jugadores/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(jugadorData)
	});
	if (!response.ok) throw new Error('Error al registrar jugador');
	return response.json();
}

export async function subirImagenJugador(archivo) {
	const formData = new FormData();
	formData.append('archivo', archivo);

	const response = await fetch(`${API_BASE}/Jugadores/upload-imagen`, {
		method: 'POST',
		body: formData
	});

	if (!response.ok) throw new Error('Error al subir imagen');
	return response.json();
}

export async function actualizarJugador(jugadorId, jugadorData) {
	const response = await fetch(`${API_BASE}/Jugadores/${jugadorId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(jugadorData)
	});
	if (!response.ok) throw new Error('Error al actualizar jugador');
	return response.json();
}

export async function eliminarJugador(jugadorId) {
	const response = await fetch(`${API_BASE}/Jugadores/${jugadorId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		let message = 'Error al eliminar jugador';
		try {
			const data = await response.json();
			if (data?.detail) message = data.detail;
		} catch {
			// no-op
		}
		throw new Error(message);
	}
	return response.json();
}

export async function fetchEquipos() {
	return getJson('/equipos/', 'Error al cargar equipos');
}

export async function fetchPartidos() {
	return getJson('/partidos/', 'Error al cargar partidos');
}

export async function fetchEstadisticas() {
	return getJson('/estadisticas/', 'Error al cargar estadísticas');
}

export async function crearPartido(partidoData) {
	const response = await fetch(`${API_BASE}/partidos/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(partidoData)
	});
	if (!response.ok) throw new Error('Error al crear partido');
	return response.json();
}

export async function actualizarPartido(partidoId, partidoData) {
	const response = await fetch(`${API_BASE}/partidos/${partidoId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(partidoData)
	});
	if (!response.ok) throw new Error('Error al actualizar partido');
	return response.json();
}

export async function eliminarPartido(partidoId) {
	const response = await fetch(`${API_BASE}/partidos/${partidoId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		let message = 'Error al eliminar partido';
		try {
			const data = await response.json();
			if (data?.detail) message = data.detail;
		} catch {
			// no-op
		}
		throw new Error(message);
	}
	return response.json();
}

export async function fetchTorneos() {
	return getJson('/torneos/', 'Error al cargar torneos');
}

export async function crearTorneo(torneoData) {
	const response = await fetch(`${API_BASE}/torneos/`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(torneoData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al crear torneo'));
	}
	return response.json();
}

export async function actualizarTorneo(torneoId, torneoData) {
	const response = await fetch(`${API_BASE}/torneos/${torneoId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(torneoData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al actualizar torneo'));
	}
	return response.json();
}

export async function eliminarTorneo(torneoId) {
	const response = await fetch(`${API_BASE}/torneos/${torneoId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al eliminar torneo'));
	}
	return response.json();
}

export async function fetchEquiposTorneo() {
	return getJson('/torneos/equipos', 'Error al cargar equipos de torneo');
}

export async function crearEquipoTorneo(equipoData) {
	const response = await fetch(`${API_BASE}/torneos/equipos`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(equipoData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al crear equipo de torneo'));
	}
	return response.json();
}

export async function actualizarEquipoTorneo(equipoTorneoId, equipoData) {
	const response = await fetch(`${API_BASE}/torneos/equipos/${equipoTorneoId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(equipoData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al actualizar equipo de torneo'));
	}
	return response.json();
}

export async function eliminarEquipoTorneo(equipoTorneoId) {
	const response = await fetch(`${API_BASE}/torneos/equipos/${equipoTorneoId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al eliminar equipo de torneo'));
	}
	return response.json();
}

export async function fetchJugadoresTorneo() {
	return getJson('/torneos/jugadores', 'Error al cargar jugadores de torneo');
}

export async function crearJugadorTorneo(jugadorData) {
	const response = await fetch(`${API_BASE}/torneos/jugadores`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(jugadorData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al agregar jugador al torneo'));
	}
	return response.json();
}

export async function actualizarJugadorTorneo(jugadorTorneoId, jugadorData) {
	const response = await fetch(`${API_BASE}/torneos/jugadores/${jugadorTorneoId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(jugadorData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al actualizar jugador de torneo'));
	}
	return response.json();
}

export async function eliminarJugadorTorneo(jugadorTorneoId) {
	const response = await fetch(`${API_BASE}/torneos/jugadores/${jugadorTorneoId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al eliminar jugador de torneo'));
	}
	return response.json();
}

export async function fetchPartidosTorneo() {
	return getJson('/torneos/partidos', 'Error al cargar partidos de torneo');
}

export async function crearPartidoTorneo(partidoData) {
	const response = await fetch(`${API_BASE}/torneos/partidos`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(partidoData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al crear partido de torneo'));
	}
	return response.json();
}

export async function actualizarPartidoTorneo(partidoTorneoId, partidoData) {
	const response = await fetch(`${API_BASE}/torneos/partidos/${partidoTorneoId}`, {
		method: 'PUT',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(partidoData)
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al actualizar partido de torneo'));
	}
	return response.json();
}

export async function eliminarPartidoTorneo(partidoTorneoId) {
	const response = await fetch(`${API_BASE}/torneos/partidos/${partidoTorneoId}`, {
		method: 'DELETE'
	});
	if (!response.ok) {
		throw new Error(await getErrorMessage(response, 'Error al eliminar partido de torneo'));
	}
	return response.json();
}
