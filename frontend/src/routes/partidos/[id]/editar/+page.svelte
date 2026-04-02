<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { toast } from '$lib/stores/toast';
	import {
		actualizarPartido,
		fetchEquipos,
		fetchEstadisticas,
		fetchJugadores,
		fetchPartidos
	} from '$lib/api';

	let equipos = [];
	let jugadores = [];
	let loading = true;
	let saving = false;
	let error = null;

	let fecha = new Date().toISOString().split('T')[0];
	let equipoLocalId = '';
	let equipoVisitanteId = '';
	let golesLocal = 0;
	let golesVisitante = 0;
	let estadisticas = [];

	const partidoId = Number($page.params.id);

	onMount(async () => {
		try {
			const [equiposData, jugadoresData, partidosData, estadisticasData] = await Promise.all([
				fetchEquipos(),
				fetchJugadores(),
				fetchPartidos(),
				fetchEstadisticas()
			]);

			equipos = equiposData;
			jugadores = jugadoresData;

			const partido = partidosData.find((p) => p.id === partidoId);
			if (!partido) {
				throw new Error('No se encontro el partido a editar');
			}

			fecha = partido.fecha;
			equipoLocalId = String(partido.equipo_local_id);
			equipoVisitanteId = String(partido.equipo_visitante_id);
			golesLocal = partido.goles_local;
			golesVisitante = partido.goles_visitante;

			estadisticas = estadisticasData
				.filter((e) => e.partido_id === partidoId)
				.map((e) => ({
					jugador_id: String(e.jugador_id),
					equipo_id: String(e.equipo_id),
					goles: e.goles
				}));
		} catch (e) {
			error = e.message;
		} finally {
			loading = false;
		}
	});

	function agregarJugador(equipoId) {
		estadisticas = [...estadisticas, { jugador_id: '', equipo_id: equipoId, goles: 0 }];
	}

	function eliminarJugador(index) {
		estadisticas = estadisticas.filter((_, i) => i !== index);
	}

	function existeJugador(jugadorId) {
		return jugadores.some((j) => String(j.id) === String(jugadorId));
	}

	function existeEquipo(equipoId) {
		return equipos.some((e) => String(e.id) === String(equipoId));
	}

	$: totalGolesLocal = estadisticas
		.filter((e) => e.equipo_id == equipoLocalId)
		.reduce((sum, e) => sum + Number(e.goles || 0), 0);

	$: totalGolesVisitante = estadisticas
		.filter((e) => e.equipo_id == equipoVisitanteId)
		.reduce((sum, e) => sum + Number(e.goles || 0), 0);

	async function guardar() {
		if (!equipoLocalId || !equipoVisitanteId) {
			toast.warning('Debes seleccionar ambos equipos');
			return;
		}

		if (equipoLocalId === equipoVisitanteId) {
			toast.warning('Los equipos deben ser diferentes');
			return;
		}

		const estadisticasValidas = estadisticas.filter((e) => e.jugador_id !== '');

		if (totalGolesLocal !== Number(golesLocal) || totalGolesVisitante !== Number(golesVisitante)) {
			toast.warning(
				`Los goles deben coincidir: Local ${golesLocal} vs ${totalGolesLocal}, Visitante ${golesVisitante} vs ${totalGolesVisitante}`
			);
			return;
		}

		saving = true;
		try {
			await actualizarPartido(partidoId, {
				fecha,
				equipo_local_id: parseInt(equipoLocalId),
				equipo_visitante_id: parseInt(equipoVisitanteId),
				goles_local: Number(golesLocal),
				goles_visitante: Number(golesVisitante),
				estadisticas: estadisticasValidas.map((e) => ({
					jugador_id: parseInt(e.jugador_id),
					equipo_id: parseInt(e.equipo_id),
					goles: Number(e.goles)
				}))
			});
			toast.success('Partido actualizado con exito');
			goto('/partidos');
		} catch (e) {
			error = e.message;
			toast.error(e.message || 'No se pudo actualizar el partido');
		} finally {
			saving = false;
		}
	}
</script>

<svelte:head>
	<title>Editar Partido - Futbol Manager</title>
</svelte:head>

<div class="max-w-4xl mx-auto space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-2xl md:text-3xl font-bold text-gray-800">✏️ Editar Partido</h1>
		<a href="/partidos" class="text-gray-600 hover:text-gray-800 text-sm md:text-base">← Volver</a>
	</div>

	{#if loading}
		<div class="text-center py-12">
			<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
			<p class="font-semibold">Error:</p>
			<p>{error}</p>
		</div>
	{:else}
		<form on:submit|preventDefault={guardar} class="space-y-6">
			<div class="bg-white rounded-lg shadow-md p-6">
				<label for="fecha-partido" class="block text-sm font-semibold text-gray-700 mb-2">Fecha del partido</label>
				<input
					id="fecha-partido"
					type="date"
					bind:value={fecha}
					required
					class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
				/>
			</div>

			<div class="bg-white rounded-lg shadow-md p-6 space-y-6">
				<h2 class="text-xl font-bold text-gray-800">Equipos y Resultado</h2>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
					<div>
						<label for="equipo-local" class="block text-sm font-semibold text-gray-700 mb-2">Equipo Local</label>
						<select
							id="equipo-local"
							bind:value={equipoLocalId}
							required
							class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 mb-4"
						>
							<option value="">Seleccionar equipo</option>
							{#if equipoLocalId && !existeEquipo(equipoLocalId)}
								<option value={String(equipoLocalId)}>
									Equipo no disponible (ID {equipoLocalId})
								</option>
							{/if}
							{#each equipos as equipo}
								<option value={String(equipo.id)}>{equipo.nombre}</option>
							{/each}
						</select>
						<label for="goles-local" class="block text-sm font-semibold text-gray-700 mb-2">Goles Local</label>
						<input
							id="goles-local"
							type="number"
							bind:value={golesLocal}
							min="0"
							required
							class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
						/>
						<p class="text-xs text-gray-600 mt-1">Goles asignados: {totalGolesLocal}</p>
					</div>

					<div>
						<label for="equipo-visitante" class="block text-sm font-semibold text-gray-700 mb-2">Equipo Visitante</label>
						<select
							id="equipo-visitante"
							bind:value={equipoVisitanteId}
							required
							class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 mb-4"
						>
							<option value="">Seleccionar equipo</option>
							{#if equipoVisitanteId && !existeEquipo(equipoVisitanteId)}
								<option value={String(equipoVisitanteId)}>
									Equipo no disponible (ID {equipoVisitanteId})
								</option>
							{/if}
							{#each equipos as equipo}
								<option value={String(equipo.id)}>{equipo.nombre}</option>
							{/each}
						</select>
						<label for="goles-visitante" class="block text-sm font-semibold text-gray-700 mb-2">Goles Visitante</label>
						<input
							id="goles-visitante"
							type="number"
							bind:value={golesVisitante}
							min="0"
							required
							class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
						/>
						<p class="text-xs text-gray-600 mt-1">Goles asignados: {totalGolesVisitante}</p>
					</div>
				</div>
			</div>

			<div class="bg-white rounded-lg shadow-md p-6 space-y-4">
				<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
					<h2 class="text-xl font-bold text-gray-800">Jugadores y goles</h2>
					<div class="flex flex-col sm:flex-row gap-2">
						<button
							type="button"
							on:click={() => agregarJugador(equipoLocalId)}
							disabled={!equipoLocalId}
							class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm disabled:bg-gray-300 disabled:cursor-not-allowed"
						>
							+ Jugador Local
						</button>
						<button
							type="button"
							on:click={() => agregarJugador(equipoVisitanteId)}
							disabled={!equipoVisitanteId}
							class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm disabled:bg-gray-300 disabled:cursor-not-allowed"
						>
							+ Jugador Visitante
						</button>
					</div>
				</div>

				{#if estadisticas.length === 0}
					<p class="text-gray-600 text-center py-4">No hay jugadores cargados</p>
				{:else}
					<div class="space-y-3">
						{#each estadisticas as est, i}
							<div class="bg-gray-50 p-3 rounded-lg">
								<div class="flex flex-col sm:flex-row sm:items-center gap-3">
								<select
									bind:value={est.jugador_id}
									required
									class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
								>
									<option value="">Seleccionar jugador</option>
									{#if est.jugador_id && !existeJugador(est.jugador_id)}
										<option value={String(est.jugador_id)}>
											Jugador no disponible (ID {est.jugador_id})
										</option>
									{/if}
									{#each jugadores as jugador}
										<option value={String(jugador.id)}>{jugador.nombre} {jugador.apodo ? `"${jugador.apodo}"` : ''}</option>
									{/each}
								</select>
									<div class="flex items-center gap-3 sm:gap-2 sm:w-auto">
										<span class="text-sm text-gray-600 font-medium min-w-20">
											{est.equipo_id == equipoLocalId ? 'Local' : 'Visitante'}
										</span>
										<input
											type="number"
											bind:value={est.goles}
											min="0"
											required
											class="w-20 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
										/>
										<button
											type="button"
											on:click={() => eliminarJugador(i)}
											class="text-red-600 hover:text-red-800 font-bold text-xl px-2"
										>
											×
										</button>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<div class="flex flex-col sm:flex-row gap-4">
				<button
					type="submit"
					disabled={saving || (Number(golesLocal) + Number(golesVisitante) > 0 && estadisticas.length === 0)}
					class="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:shadow-lg transition-all disabled:bg-gray-300 disabled:cursor-not-allowed"
				>
					{saving ? 'Guardando...' : 'Guardar cambios'}
				</button>
				<a
					href="/partidos"
					class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold px-6 py-3 rounded-lg text-center transition-all"
				>
					Cancelar
				</a>
			</div>
		</form>
	{/if}
</div>
