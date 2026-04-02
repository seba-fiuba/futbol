<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { fetchEquipos, fetchEstadisticas, fetchJugadores, fetchPartidos } from '$lib/api';

	let loading = true;
	let error = null;

	let partido = null;
	let equipos = [];
	let jugadores = [];
	let estadisticasPartido = [];

	const partidoId = Number($page.params.id);

	onMount(async () => {
		try {
			const [partidosData, equiposData, jugadoresData, estadisticasData] = await Promise.all([
				fetchPartidos(),
				fetchEquipos(),
				fetchJugadores(),
				fetchEstadisticas()
			]);

			partido = partidosData.find((p) => p.id === partidoId) || null;
			if (!partido) {
				throw new Error('No se encontro el partido');
			}

			equipos = equiposData;
			jugadores = jugadoresData;
			estadisticasPartido = estadisticasData.filter((e) => e.partido_id === partidoId);
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	function getEquipoNombre(equipoId) {
		const equipo = equipos.find((e) => e.id === equipoId);
		return equipo ? equipo.nombre : 'Desconocido';
	}

	function getJugador(jugadorId) {
		return jugadores.find((j) => j.id === jugadorId) || null;
	}

	function getJugadorNombre(jugadorId) {
		const jugador = getJugador(jugadorId);
		return jugador ? jugador.nombre : `Jugador #${jugadorId}`;
	}

	function getJugadorImagen(jugadorId) {
		const jugador = getJugador(jugadorId);
		return jugador?.imagen || null;
	}

	function formatFecha(fecha) {
		return new Date(fecha).toLocaleDateString('es-AR', {
			day: '2-digit',
			month: '2-digit',
			year: 'numeric'
		});
	}

	$: estadisticasAgrupadas = estadisticasPartido
		.reduce((acc, est) => {
			const key = `${est.jugador_id}-${est.equipo_id}`;
			const existente = acc.find((item) => item.key === key);
			if (existente) {
				existente.goles += Number(est.goles || 0);
			} else {
				acc.push({
					key,
					jugador_id: est.jugador_id,
					equipo_id: est.equipo_id,
					goles: Number(est.goles || 0)
				});
			}
			return acc;
		}, [])
		.sort((a, b) => b.goles - a.goles || getJugadorNombre(a.jugador_id).localeCompare(getJugadorNombre(b.jugador_id)));

	$: jugadoresLocal = estadisticasAgrupadas.filter((e) => e.equipo_id === partido?.equipo_local_id);
	$: jugadoresVisitante = estadisticasAgrupadas.filter((e) => e.equipo_id === partido?.equipo_visitante_id);
</script>

<svelte:head>
	<title>Detalle de Partido - Futbol Manager</title>
</svelte:head>

<div class="max-w-5xl mx-auto space-y-6">
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
		<h1 class="text-2xl md:text-3xl font-bold text-gray-800">📋 Detalle del Partido</h1>
		<a href="/partidos" class="text-gray-600 hover:text-gray-800 text-sm md:text-base">← Volver</a>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
			<p class="mt-4 text-gray-600">Cargando detalle...</p>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
		</div>
	{:else}
		<div class="bg-white rounded-lg shadow-md p-4 md:p-6 space-y-4">
			<p class="text-sm text-gray-600 font-medium">{formatFecha(partido.fecha)}</p>
			<div class="grid grid-cols-1 md:grid-cols-3 gap-4 items-center text-center">
				<div>
					<h2 class="text-2xl font-bold text-gray-800">{getEquipoNombre(partido.equipo_local_id)}</h2>
					<p class="text-sm text-gray-600">Local</p>
				</div>
				<div>
					<div class="text-4xl font-extrabold text-green-600">
						{partido.goles_local} - {partido.goles_visitante}
					</div>
				</div>
				<div>
					<h2 class="text-2xl font-bold text-gray-800">{getEquipoNombre(partido.equipo_visitante_id)}</h2>
					<p class="text-sm text-gray-600">Visitante</p>
				</div>
			</div>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<h3 class="text-xl font-bold text-gray-800 mb-4">{getEquipoNombre(partido.equipo_local_id)} (Local)</h3>
				{#if jugadoresLocal.length === 0}
					<p class="text-gray-600">No hay jugadores cargados.</p>
				{:else}
					<div class="space-y-3">
						{#each jugadoresLocal as item}
							<div class="flex items-center justify-between bg-gray-50 rounded-lg p-3">
								<div class="flex items-center gap-3 min-w-0">
									{#if getJugadorImagen(item.jugador_id)}
										<img src={getJugadorImagen(item.jugador_id)} alt={getJugadorNombre(item.jugador_id)} class="w-9 h-9 rounded-full object-cover" />
									{:else}
										<div class="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center">👤</div>
									{/if}
									<p class="font-medium text-gray-800 truncate">{getJugadorNombre(item.jugador_id)}</p>
								</div>
								<p class="font-bold text-green-700">⚽ {item.goles}</p>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<div class="bg-white rounded-lg shadow-md p-4 md:p-6">
				<h3 class="text-xl font-bold text-gray-800 mb-4">{getEquipoNombre(partido.equipo_visitante_id)} (Visitante)</h3>
				{#if jugadoresVisitante.length === 0}
					<p class="text-gray-600">No hay jugadores cargados.</p>
				{:else}
					<div class="space-y-3">
						{#each jugadoresVisitante as item}
							<div class="flex items-center justify-between bg-gray-50 rounded-lg p-3">
								<div class="flex items-center gap-3 min-w-0">
									{#if getJugadorImagen(item.jugador_id)}
										<img src={getJugadorImagen(item.jugador_id)} alt={getJugadorNombre(item.jugador_id)} class="w-9 h-9 rounded-full object-cover" />
									{:else}
										<div class="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center">👤</div>
									{/if}
									<p class="font-medium text-gray-800 truncate">{getJugadorNombre(item.jugador_id)}</p>
								</div>
								<p class="font-bold text-green-700">⚽ {item.goles}</p>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>
